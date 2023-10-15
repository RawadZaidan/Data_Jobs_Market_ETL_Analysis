from database_handler import execute_query, create_connection,return_create_statement_from_df_stg
from lookup import ErrorHandling, InputTypes, DESTINATION_SCHEMA, SQL_PREHOOK_COMMANDS_PATH
from database_handler import return_insert_into_sql_statement_from_df_stg
from logging_handler import show_error_message
import pandas as pd
import os

def execute_sql_folder(db_session, sql_command_directory_path='sql_commands'):
    try:
        sql_files = [sqlfile for sqlfile in os.listdir(sql_command_directory_path) if sqlfile.endswith('.sql')]
        sorted_sql_files =  sorted(sql_files)
        for sql_file in sorted_sql_files:
            with open(os.path.join(sql_command_directory_path,sql_file), 'r') as file:
                sql_query = file.read()
                return_val = execute_query(db_session= db_session, query= sql_query)
                if not return_val == ErrorHandling.NO_ERROR:
                    raise Exception(" SQL File Error on SQL FILE = " +  str(sql_file))
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.PREHOOK_SQL_ERROR
        show_error_message(error_prefix.value, suffix)

def alter_column_type(db_session, table_name, column, new_type='TEXT',schema=DESTINATION_SCHEMA.DESTINATION_NAME.value):
    query = f'''ALTER TABLE {schema}.{table_name}
               ALTER COLUMN {column} TYPE {new_type};'''
    execute_query(db_session, query)

def prehook_local_files_into_pg(db_session):
    
    df_jobs = pd.read_csv('csvs/agg_all.csv')
    stmnt = return_create_statement_from_df_stg(df_jobs, 'jobs')
    execute_query(db_session, stmnt)
    alter_column_type(db_session, 'stg_jobs', 'id')
    queries = return_insert_into_sql_statement_from_df_stg(df_jobs, 'jobs')
    for query in queries:
        execute_query(db_session, query)

def prehook():

    db_session = create_connection()

    execute_sql_folder(db_session)

    prehook_local_files_into_pg()
