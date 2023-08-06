import csv
import io
import os
import re
import datetime
import traceback
from textwrap import dedent
from types import SimpleNamespace
from typing import Union, Any, Dict, List
from collections import defaultdict

from src.db import DB, Query, get_db_and_query_classes

class QueryList(list):

    actions: Dict[str, str] = {
        'e': 'query',
        't': 'create_table_stmt',
        'v': 'create_view_stmt',
        'm': 'materialize_view_stmt',
        'check': 'run_check_stmt',
        's': 'skip'
    }

    def __init__(self, config: SimpleNamespace, csv_string: str, dependencies: List[Dict]):
        DBClass, QueryClass = get_db_and_query_classes(config)
        self.config = config
        self.db: DB = DBClass(config)
        given_order = []
        available_set = {}
        for query in csv.DictReader(io.StringIO(csv_string.strip()), delimiter=';'):
            if not query['schema_name'].startswith('#'):
                given_order.append(query)
                available_set[(query['schema_name'], query['table_name'])] = query
        
        indexed_dependencies = defaultdict(list)
        for d in dependencies:
            indexed_dependencies[(d['dependent_schema'], d['dependent_table'])].append(
                (d['source_schema'], d['source_table'])
            )

        def add_query(schema, table):
            if (schema, table) in indexed_dependencies:
                for dep in indexed_dependencies[(schema, table)]:
                    add_query(*dep)
            if (schema, table) in available_set:
                self.append(QueryClass(config, **available_set[(schema, table)]))
                del available_set[(schema, table)]
        
        for query in given_order:
            add_query(query['schema_name'], query['table_name'])

    @staticmethod
    def from_csv_files(config: SimpleNamespace, csv_files: List[str], dependencies: List[Dict]) -> "QueryList":
        """ Creates a query list from a list of CSV file names, passed in as Command Line Arguments
        """
        if not isinstance(csv_files, list):
            csv_files = [csv_files]
        print('read query lists from: {}'.format(', '.join(csv_files)))
        csv_string = ['schema_name;table_name;action']
        for file in csv_files:
            file_path = f'{config.sql_path}/{file}.csv'
            with open(file_path, 'r') as f:
                csv_string.append(f.read().strip())
        return QueryList(config, '\n'.join(csv_string), dependencies)


    def test(self, staging=False):
        """ Test exeution of query list, if `test` is passed into the arguments
        """

        if hasattr(self.config, 'test_schema_prefix'):
            schema_prefix = self.config.test_schema_prefix
        else:
            schema_prefix = Query.default_schema_prefix
        schema_names = set(query.schema_name for query in self)
        full_table_names = set(query.full_table_name for query in self)
        # Recreate schemata
        for schema_name in schema_names:
            statements = f"""
            DROP SCHEMA IF EXISTS {schema_prefix}{schema_name} CASCADE;
            CREATE SCHEMA {schema_prefix}{schema_name}
            """
            for stmt in statements.split(';'):
                # Use the query db-specific executor
                self.db.execute(stmt)
        
        # Change all queries to use schema_prefix
        # Plus change query actions:
        # query => s (skip)
        # *     => view
        for query in self:
            query.schema_prefix = schema_prefix
            for full_table_name in full_table_names:
                query.query = query.query.replace(' ' + full_table_name, ' ' + schema_prefix + full_table_name)

            if staging is False:
                if query.action == 'e':
                    query.action = 's'
                else:
                    query.action = 'v'
        self.execute()

    def execute(self):
        """ Execute every statement from every query
        """
        run_start = datetime.datetime.now()
        for query in self:
            start = datetime.datetime.now()
            print(query)
            if query.action in QueryList.actions:
                # Any of 'query', 'create_table_stmt', 'create_view_stmt', 'materialize_view_stmt', 'run_check'
                stmt_type = QueryList.actions[query.action]
                # Get list of individual specific statements and process them
                for stmt in getattr(query, stmt_type).split(';'):
                    if stmt.strip():
                        self.db.execute(stmt, query)
                        # Perform any tests
                        assertion = query.assertion
                        if assertion:
                            assertion(rows=self.db.fetchall())
            print(datetime.datetime.now() - start)
        print('Run finished in {}'.format(datetime.datetime.now() - run_start))
