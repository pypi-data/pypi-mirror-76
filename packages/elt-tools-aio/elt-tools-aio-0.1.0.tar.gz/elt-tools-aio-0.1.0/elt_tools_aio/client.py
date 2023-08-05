"""Generic Client for interacting with data sources."""
from typing import *
import asyncio
import time
import datetime
import logging
import math
from sqlalchemy import MetaData, Table
from sqlalchemy.exc import OperationalError
from psycopg2.errors import SerializationFailure
from typing import Dict, Set, List, Tuple, Optional
from elt_tools_aio.engines import engine_from_settings


def _construct_where_clause_from_timerange(
        start_datetime: datetime.datetime = None,
        end_datetime: datetime.datetime = None,
        timestamp_fields: List[str] = None,
        stick_to_dates: bool = False
):
    where_clause = ""

    if stick_to_dates and start_datetime == end_datetime:
        msg = "The date range for dates is inclusive of the start date and exclusive of the end date." \
              "Since your start and end date range is the same, your query will be meaningless."
        raise ValueError(msg)

    if (not timestamp_fields and start_datetime) or (not timestamp_fields and end_datetime):
        msg = "You've passed in a time range, but no timestamp field names."
        logging.warning(msg)
        return ''

    if stick_to_dates:
        fmt_string = "%Y-%m-%d"
    else:
        fmt_string = "%Y-%m-%d %H:%M:%S"

    if start_datetime:
        start_datetime = start_datetime.strftime(fmt_string)
    if end_datetime:
        end_datetime = end_datetime.strftime(fmt_string)

    if timestamp_fields and start_datetime and end_datetime:
        where_clause += " WHERE " + " OR ".join([
            f"({timestamp_field} >= '{start_datetime}' AND {timestamp_field} < '{end_datetime}')"
            for timestamp_field in timestamp_fields
        ])
        return where_clause

    if timestamp_fields and start_datetime:
        where_clause += " WHERE " + " AND ".join([
            f"{timestamp_field} >= '{start_datetime}'"
            for timestamp_field in timestamp_fields
        ])
    if timestamp_fields and end_datetime:
        where_clause += " WHERE " + " AND ".join([
            f"{timestamp_field} < '{end_datetime}'"
            for timestamp_field in timestamp_fields
        ])
    return where_clause


class DataClient:

    @classmethod
    def update_settings(cls, item_name):
        """

        :param item_name: Corresponds to settings class-attribute name
        :return:
        """

    def __init__(self, engine):
        self.engine = engine
        self.metadata = MetaData(bind=self.engine)
        self.table_name = None
        self._tables = {}

    @classmethod
    def from_settings(cls, database_settings: Dict, db_key):
        return cls(engine_from_settings(db_key, database_settings=database_settings))

    async def get_table(self, table_name):
        logging.debug(f"Inspecting table {table_name}")
        t = Table(table_name, self.metadata, autoload_with=self.engine)  #, autoload_with=self.engine.sync_engine)
        return t

    async def table(self, table_name):
        """Introspect Table object from engine metadata."""
        if table_name in self._tables:
            logging.debug(f"Using cached definition of table {table_name}")
            return self._tables[table_name]
        else:
            self._tables[table_name] = await self.get_table(table_name)
            logging.debug("Introspection done.")
            return self._tables[table_name]

    async def insert_rows(self, rows, table=None, replace=None):
        """Insert rows into table."""
        if replace:
            await self.engine.execute(f'TRUNCATE TABLE {table}')
        self.table_name = table
        _table = self.table(table)
        await self.engine.execute(_table.insert(), rows)
        return self.construct_response(rows, table)

    async def delete_rows(self, table_name, key_field, primary_keys=None):
        if not primary_keys:
            logging.error("Pass in the primary keys to delete.")
            return

        def format_primary_key(key):
            if isinstance(key, int):
                return str(key)
            else:
                return f"'{str(key)}'"

        query = f"""
        DELETE {table_name} WHERE {key_field} IN ({','.join(map(format_primary_key, primary_keys))})
        """
        logging.info(query)
        await self.query(query)

    async def fetch_rows(self, query):
        """Fetch all rows via query."""
        async with self.engine.connect() as connection:
            row_proxy = await connection.execute(query)
            rows = await row_proxy.fetchall()
        # await connection.close()
        return rows

    async def query(self, query):
        return [dict(r) for r in await self.fetch_rows(query)]

    @staticmethod
    def construct_response(rows, table):
        """Summarize results of an executed query."""
        columns = rows[0].keys()
        column_names = ", ".join(columns)
        num_rows = len(rows)
        return f'Inserted {num_rows} rows into `{table}` with {len(columns)} columns: {column_names}'

    async def count(
            self,
            table_name,
            field_name=None,
            start_datetime: datetime.datetime = None,
            end_datetime: datetime.datetime = None,
            timestamp_fields: List[str] = None,
            stick_to_dates: bool = False,
            recursion_count=0,
            timeout=60,
    ) -> int:
        """
        Optionally pass in timestamp fields and time range to limit the query_range.
        """
        if recursion_count > 0:
            timeout = 999
        if recursion_count == 3:
            raise ValueError("Could not complete count for table %s, too many failed attempts." % table_name)

        if not field_name:
            field_name = "*"

        unfiltered_count_query = f"""
        SELECT COUNT({field_name}) AS count FROM {table_name}
        """
        where_clause = _construct_where_clause_from_timerange(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            timestamp_fields=timestamp_fields,
            stick_to_dates=stick_to_dates,
        )
        count_query = unfiltered_count_query + where_clause
        logging.debug("Count query is %s" % count_query)
        try:
            result_set = await asyncio.wait_for(self.query(count_query), timeout=timeout)
            result = result_set[0]['count']
        # sometimes with postgres dbs we encounter SerializationFailure when we query the slave and master
        # interrupts it. In this case, we sub-divide the query time range.
        except (OperationalError, SerializationFailure, asyncio.TimeoutError) as e:
            if isinstance(e, OperationalError) and 'SerializationFailure' not in str(e):
                raise
            if isinstance(e, TimeoutError):
                time.sleep(10)
            if where_clause:
                range_len = math.floor((end_datetime - start_datetime) / datetime.timedelta(hours=24))
                logging.info(
                    "Encountered exception with count query across %d days. Aggregating over single days. %s" % (
                        range_len, str(e)))
                range_split = [start_datetime + datetime.timedelta(days=n) for n in range(range_len)] + [end_datetime]
                result = 0
                for sub_start, sub_end in zip(range_split, range_split[1:]):
                    sub_count = await self.count(
                        table_name,
                        field_name,
                        start_datetime=sub_start,
                        end_datetime=sub_end,
                        timestamp_fields=timestamp_fields,
                        stick_to_dates=stick_to_dates,
                        recursion_count=recursion_count + 1,
                    )
                    result += sub_count
            else:
                raise
        return result

    async def get_primary_key(self, table_name: str) -> Optional[str]:
        """
        Inspect the table to find the primary key.
        """
        table = await self.table(table_name)
        prim_key = table.primary_key
        if prim_key:
            key_cols = list(prim_key.columns)
            if len(key_cols) > 1:
                logging.warning("Currently this toolset only supports sole primary keys. "
                                f"Found keys {key_cols} for {table_name}.")
                return None
            if key_cols:
                primary_key_field_name = key_cols[0].name
                logging.debug(f'Found primary key of {table_name} is {primary_key_field_name}.')
                return primary_key_field_name
            else:
                return None

    async def get_all_tables(self) -> List[str]:
        """
        List all the table names present in the schema definition.
        """
        source_db_tables = []
        query = '''
              SELECT table_name
                FROM {bq_schema}INFORMATION_SCHEMA.TABLES
              ORDER BY table_name
            '''.format(
            bq_schema=self.engine._engine.url.database + '.' if self.engine._engine.name == 'bigquery' else ''
        )
        tables = await self.fetch_rows(query)
        for table in tables:
            source_db_tables.append(table[0])
        return source_db_tables

    async def find_duplicate_keys(self, table_name, key_field):
        """Find if a table has duplicates by a certain column, if so return all the instances that
        have duplicates together with their counts."""
        query = f"""
        SELECT {key_field}, COUNT({key_field}) as count
        FROM {table_name}
        GROUP BY 1
        HAVING COUNT({key_field}) > 1;
        """
        return await self.fetch_rows(query)

    async def _find_partition_expression(self, table_name):
        """
           Note: this currently only supports Google Biquery
        """
        partition_field_sql = f"""
            SELECT column_name, data_type
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE table_name = '{table_name}'
              AND is_partitioning_column = 'YES';
        """
        partition_field_result = await self.query(partition_field_sql)
        partition_field_expr = None
        partition_field_name = None
        partition_field_type = None
        for row in partition_field_result:
            if partition_field_name:
                raise ValueError("Expecting one partition field, found multiple.")
            partition_field_name = row['column_name']
            partition_field_type = row['data_type']

        if partition_field_type == 'TIMESTAMP':
            partition_field_expr = f'DATE({partition_field_name})'
        elif partition_field_type == 'DATE':
            partition_field_expr = partition_field_name
        else:
            raise ValueError('Expected partition field to be either DATE OR TIMESTAMP.'
                             f' "{partition_field_type}" not supported. ')

        if partition_field_expr:
            return f'PARTITION BY {partition_field_expr}'
        else:
            return None

    async def _find_cluster_expr(self, table_name):
        """
           Note: this currently only supports Google Biquery
        """

        cluster_fields_sql = f"""
           SELECT column_name
           FROM INFORMATION_SCHEMA.COLUMNS
           WHERE table_name = '{table_name}'
            AND clustering_ordinal_position IS NOT NULL
           ORDER BY clustering_ordinal_position ASC;
        """
        cluster_fields_result = await self.query(cluster_fields_sql)
        cluster_field_exp = ','.join([r['column_name'] for r in cluster_fields_result])

        if cluster_field_exp:
            return 'CLUSTER BY ' + cluster_field_exp
        else:
            return None

    async def remove_duplicate_keys_from_bigquery(self, table_name, key_field):
        """Remove any duplicate records when comparing primary keys.
           Note: this currently only supports Google Biquery
        """
        dups = await self.find_duplicate_keys(table_name, key_field)
        if dups:
            logging.info(f"Removing duplicates from {table_name}: {str(dups)}")
        else:
            logging.info(f"No duplicates found in {table_name}.")
            return

        partition_exp = await self._find_partition_expression(table_name)
        cluster_exp = await self._find_cluster_expr(table_name)

        sql = f"""
                    CREATE OR REPLACE TABLE {table_name}
                    {partition_exp if partition_exp else ''}
                    {cluster_exp if cluster_exp else ''}
                    AS
                    SELECT k.*
                    FROM (
                      SELECT ARRAY_AGG(row LIMIT 1)[OFFSET(0)] k 
                      FROM {table_name} row
                      GROUP BY {key_field}
                    )
                """
        logging.info(sql)
        await self.query(sql)
        logging.info("Duplicates removed.")


class DataClientFactory:

    def __init__(self, database_settings):
        self.database_settings = database_settings

    def __call__(self, db_key=None):
        return DataClient.from_settings(
            self.database_settings,
            db_key,
        )


class ELTDBPair:

    def __init__(self, name: str, source: DataClient, target: DataClient):
        self.name = name
        self.source = source
        self.target = target

    @classmethod
    def from_settings(cls, elt_pair_settings, database_settings, pair_key, name=None):
        if not name:
            name = pair_key
        if not pair_key:
            pair_key = name
        source_target_settings = elt_pair_settings[pair_key]
        source_client = DataClient.from_settings(database_settings, source_target_settings['source'])
        target_client = DataClient.from_settings(database_settings, source_target_settings['target'])
        return cls(name, source_client, target_client)

    def __repr__(self):
        return self.name

    async def compare_counts(
            self,
            table_name,
            field_name=None,
            start_datetime: datetime.datetime = None,
            end_datetime: datetime.datetime = None,
            timestamp_fields: List[str] = None,
            stick_to_dates: bool = False
    ) -> int:
        return await self.target.count(
            table_name,
            field_name=field_name,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            timestamp_fields=timestamp_fields,
            stick_to_dates=stick_to_dates,
        ) - await self.source.count(
            table_name,
            field_name=field_name,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            timestamp_fields=timestamp_fields,
            stick_to_dates=stick_to_dates,
        )

    async def _find_orphans(
            self,
            table_name,
            key_field,
            start_datetime: datetime.datetime = None,
            end_datetime: datetime.datetime = None,
            timestamp_fields: List[str] = None,
            stick_to_dates: bool = False,
            **kwargs,
    ) -> Set:
        """
        Find orphaned records in target for which their source parents were deleted.
        Optionally pass in timestamp fields and time range to limit the amount of records
        to compare for orphans (for use on large tables).
        """
        orphans, _ = await self._find_orphans_and_missing_in_target(
            table_name,
            key_field,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            timestamp_fields=timestamp_fields,
            stick_to_dates=stick_to_dates,
            **kwargs,
        )
        return orphans

    async def find_orphans(
            self,
            table_name,
            key_field,
            start_datetime: datetime.datetime = None,
            end_datetime: datetime.datetime = None,
            timestamp_fields: List[str] = None,
            stick_to_dates: bool = False,
            **kwargs,
    ):
        orphans = await self.find_by_recursive_date_range_bifurcation(
            table_name,
            key_field,
            self._find_orphans,
            bifurcation_against='target',
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            timestamp_fields=timestamp_fields,
            stick_to_dates=stick_to_dates,
            **kwargs,
        )
        return orphans

    async def remove_orphans_from_target(
            self,
            table_name,
            key_field,
            start_datetime: datetime.datetime = None,
            end_datetime: datetime.datetime = None,
            timestamp_fields: List[str] = None,
            stick_to_dates: bool = False,
            dry_run: bool = False,
            **kwargs,
    ):
        orphans = await self.find_orphans(
            table_name,
            key_field,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            timestamp_fields=timestamp_fields,
            stick_to_dates=stick_to_dates,
            **kwargs,
        )
        if not dry_run:
            await self.target.delete_rows(table_name, key_field, primary_keys=orphans)

        return orphans

    async def find_by_recursive_date_range_bifurcation(
            self,
            table_name,
            key_field,
            find_func,
            bifurcation_against='target',
            start_datetime: datetime.datetime = None,
            end_datetime: datetime.datetime = None,
            timestamp_fields: List[str] = None,
            stick_to_dates: bool = False,
            thres=100000,
            max_segment_size=None,
            min_segment_size=datetime.timedelta(days=1),
            dry_run=False,
            skip_based_on_count=False,
    ) -> Set[Union[str, int]]:
        """
        Do binary search on table by recursively bifurcating the date range
        until the number of records in that range drops below the threshold.
        Once, below the threshold, apply the specified find function.
        :param table_name:
        :param key_field:
        :param find_func: Find function to apply. Must take same params as this function, except `func` param.
                     Must return a set of primary keys of the records it found.
        :param bifurcation_against: Either 'source' or 'target'. Choose which DB in the pair you want to split the data
                                    range against.
        :param start_datetime:
        :param end_datetime:
        :param timestamp_fields:
        :param stick_to_dates:
        :param thres:
        :param max_segment_size: datetime.timedelta object to indicate the largest timerange to query on. Good for big tables with count timeouts.
        :param min_segment_size:
        :param dry_run:
        :return: Set of primary keys of whatever is found
        """
        if not timestamp_fields:
            logging.warning("For a more efficient search, specify the timestamp field(s).")
            return await find_func(
                table_name,
                key_field,
                stick_to_dates=stick_to_dates,
                skip_based_on_count=skip_based_on_count,
            )

        bifurcation_against_lookup = {
            'source': self.source,
            'target': self.target,
        }
        # If time range is not set, fetch it from the target database
        if not start_datetime:
            query = """
            SELECT {select_stmt}
            FROM {table_name}
            """.format(
                select_stmt=', '.join(map(lambda x: 'MIN({0}) AS {0} '.format(x), timestamp_fields)),
                table_name=table_name,
            )
            result = await bifurcation_against_lookup[bifurcation_against].query(query)
            start_datetime = min(result[0].values())
            # make timezone aware, assume UTC
            if not end_datetime.tzinfo:
                end_datetime = end_datetime.replace(tzinfo=datetime.timezone.utc)
        if not end_datetime:
            query = """
            SELECT {select_stmt}
            FROM {table_name}
            """.format(
                select_stmt=', '.join(map(lambda x: 'MAX({0}) AS {0} '.format(x), timestamp_fields)),
                table_name=table_name,
            )
            result = await bifurcation_against_lookup[bifurcation_against].query(query)
            end_datetime = max(result[0].values())
            # make timezone aware, assume UTC
            if not end_datetime.tzinfo:
                end_datetime = end_datetime.replace(tzinfo=datetime.timezone.utc)

        if stick_to_dates:
            if start_datetime:
                start_datetime = start_datetime.date()
            if end_datetime:
                end_datetime = end_datetime.date()

        # recurse on smaller chunks of time-range is larger than limit
        if (end_datetime - start_datetime) > max_segment_size:
            range_len = math.floor((end_datetime - start_datetime) / max_segment_size)
            range_split = [start_datetime + max_segment_size for n in range(range_len)] + [end_datetime]
            find_result = set()
            for sub_start, sub_end in zip(range_split, range_split[1:]):
                find_result |= await self.find_by_recursive_date_range_bifurcation(
                    table_name,
                    key_field,
                    find_func,
                    bifurcation_against=bifurcation_against,
                    start_datetime=sub_start,
                    end_datetime=sub_end,
                    timestamp_fields=timestamp_fields,
                    stick_to_dates=stick_to_dates,
                    thres=thres,
                    max_segment_size=max_segment_size,
                    min_segment_size=min_segment_size,
                    dry_run=dry_run,
                    skip_based_on_count=skip_based_on_count
                )
            return find_result

        def avg_datetime(start, end):
            return start + (end - start) / 2

        def bifurcate_time_range(start, end):
            halfway = avg_datetime(start, end)
            return start, halfway, end

        find_result = set()
        count1 = count2 = 0
        start, halfway, end = bifurcate_time_range(start_datetime, end_datetime)
        logging.debug(f"Start date is : {start}")
        logging.debug(f"Halfway date is : {halfway}")
        logging.debug(f"End date is : {end}")

        if start != halfway:
            try:
                count1 = await bifurcation_against_lookup[bifurcation_against].count(
                    table_name,
                    field_name=key_field,
                    start_datetime=start,
                    end_datetime=halfway,
                    timestamp_fields=timestamp_fields,
                    stick_to_dates=stick_to_dates,
                )
                logging.debug(f"Count of range 1 is {count1}")
            except TimeoutError:
                # if count times out, assume it's larger than the threshold
                count1 = thres + 1
                logging.debug(f"Count 1 timed out, assuming greater than threshold of {thres}.")

        if end != halfway:
            try:
                count2 = await bifurcation_against_lookup[bifurcation_against].count(
                    table_name,
                    field_name=key_field,
                    start_datetime=halfway,
                    end_datetime=end,
                    timestamp_fields=timestamp_fields,
                    stick_to_dates=stick_to_dates,
                )
                logging.debug(f"Count of range 2 is {count2}")
            except TimeoutError:
                # if count times out, assume it's larger than the threshold
                count2 = thres + 1
                logging.debug(f"Count 2 timed out, assuming greater than threshold of {thres}.")

        # exit conditions
        if start == halfway or end == halfway or (halfway - start) < min_segment_size:
            return await find_func(
                table_name,
                key_field,
                start_datetime=start,
                end_datetime=end,
                timestamp_fields=timestamp_fields,
                stick_to_dates=stick_to_dates,
                dry_run=dry_run,
                skip_based_on_count=skip_based_on_count,
            )
        if count1 == 0 and count2 == 0:
            return set()
        if count1 < thres and count2 < thres:
            return await find_func(
                table_name,
                key_field,
                start_datetime=start,
                end_datetime=halfway,
                timestamp_fields=timestamp_fields,
                stick_to_dates=stick_to_dates,
                dry_run=dry_run,
                skip_based_on_count=skip_based_on_count,
            ) | await find_func(
                table_name,
                key_field,
                start_datetime=halfway,
                end_datetime=end,
                timestamp_fields=timestamp_fields,
                stick_to_dates=stick_to_dates,
                dry_run=dry_run,
                skip_based_on_count=skip_based_on_count,
            )

        # recursion conditions
        if count1 >= thres or count2 >= thres:
            find_result |= await self.find_by_recursive_date_range_bifurcation(
                table_name,
                key_field,
                find_func=find_func,
                start_datetime=start,
                end_datetime=halfway,
                timestamp_fields=timestamp_fields,
                stick_to_dates=stick_to_dates,
                thres=thres,
                skip_based_on_count=skip_based_on_count,
                max_segment_size=max_segment_size,
                min_segment_size=min_segment_size,
            ) | await self.find_by_recursive_date_range_bifurcation(
                table_name,
                key_field,
                find_func=find_func,
                start_datetime=halfway,
                end_datetime=end,
                timestamp_fields=timestamp_fields,
                stick_to_dates=stick_to_dates,
                thres=thres,
                skip_based_on_count=skip_based_on_count,
                max_segment_size=max_segment_size,
                min_segment_size=min_segment_size,
            )

        return find_result

    async def _find_orphans_and_missing_in_target(
            self,
            table_name: str,
            key_field: str,
            start_datetime: datetime.datetime = None,
            end_datetime: datetime.datetime = None,
            timestamp_fields: List[str] = None,
            stick_to_dates: bool = False,
            skip_based_on_count: bool = True,
            **kwargs,
    ) -> Tuple[Set, Set]:
        """
        Find orphaned records and missing records in target compared to the source.
        Optionally pass in timestamp fields and time range to limit the amount of records
        to compare for missing records.
        """
        if key_field is None:
            return {}

        all_ids_query = f"""
            SELECT {key_field} AS id FROM {table_name}
        """

        where_clause = _construct_where_clause_from_timerange(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            timestamp_fields=timestamp_fields,
            stick_to_dates=stick_to_dates,
        )
        all_ids_query += where_clause
        logging.debug("Id lookup for find query: %s" % all_ids_query)

        # First compare counts on limited date range to skip id comparison if no difference
        if where_clause and skip_based_on_count:
            count_diff = await self.compare_counts(
                table_name,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                timestamp_fields=timestamp_fields,
                stick_to_dates=stick_to_dates,
            )
            if count_diff == 0:
                return set(), set()

        def format_id(row):
            id = row['id']
            if isinstance(id, int):
                return id
            else:
                return str(id)  # cast to str if UUID

        target_rows = await self.target.fetch_rows(all_ids_query)
        target_ids = set(map(format_id, target_rows))

        source_rows = await self.source.fetch_rows(all_ids_query)
        source_ids = set(map(format_id, source_rows))

        missing = source_ids - target_ids
        orphans = target_ids - source_ids
        return orphans, missing

    async def _find_missing(
            self,
            table_name,
            key_field,
            start_datetime: datetime.datetime = None,
            end_datetime: datetime.datetime = None,
            timestamp_fields: List[str] = None,
            stick_to_dates: bool = False,
            **kwargs,
    ) -> Set:
        """
        Find missing records in target for which their source parents were deleted.
        Optionally pass in timestamp fields and time range to limit the amount of records
        to compare for missing records.
        """
        _, missing = await self._find_orphans_and_missing_in_target(
            table_name,
            key_field,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            timestamp_fields=timestamp_fields,
            stick_to_dates=stick_to_dates,
            **kwargs,
        )
        return missing

    async def find_missing(
            self,
            table_name,
            key_field,
            start_datetime: Optional[datetime.datetime] = None,
            end_datetime: Optional[datetime.datetime] = None,
            timestamp_fields: List[str] = None,
            stick_to_dates: Optional[bool] = False,
            **kwargs,
    ) -> Set[Union[str, int]]:
        """
        Find primary keys of missing records in target for which their source parents were deleted.
        Optionally pass in timestamp fields and time range to limit the amount of records
        to compare for missing records.
        """
        missing = await self.find_by_recursive_date_range_bifurcation(
            table_name,
            key_field,
            self._find_missing,
            bifurcation_against='source',
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            timestamp_fields=timestamp_fields,
            stick_to_dates=stick_to_dates,
            **kwargs,
        )
        return missing

    async def get_common_tables(self):
        source_tables = set(await self.source.get_all_tables())
        target_tables = set(await self.target.get_all_tables())
        return sorted(source_tables.intersection(target_tables))

    def fill_missing_target_records(self):
        pass

    def remove_duplicates_from_target(self):
        pass


class ELTDBPairFactory:

    def __init__(self, elt_pair_settings, database_settings):
        self.elt_pair_settings = elt_pair_settings
        self.database_settings = database_settings

    def __call__(self, name=None, pair_key=None):
        return ELTDBPair.from_settings(
            self.elt_pair_settings,
            self.database_settings,
            pair_key,
            name=name,
        )
