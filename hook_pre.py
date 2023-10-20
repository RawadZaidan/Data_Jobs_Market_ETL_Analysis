from database_handler import execute_query, create_connection,return_create_statement_from_df_stg
from lookup import ErrorHandling, InputTypes, DESTINATION_SCHEMA, SQL_PREHOOK_COMMANDS_PATH
from database_handler import return_insert_into_sql_statement_from_df_stg
from logging_handler import show_error_message
import pandas as pd
import datetime
import os

def execute_sql_folder(db_session, sql_command_directory_path='sql_commands'):
    try:
        sql_files = [sqlfile for sqlfile in os.listdir(sql_command_directory_path) if sqlfile.endswith('.sql')]
        sorted_sql_files = sorted(sql_files)
        errors = []

        for sql_file in sorted_sql_files:
            file_path = os.path.join(sql_command_directory_path, sql_file)
            with open(file_path, 'r') as file:
                sql_query = file.read()
                return_val = execute_query(db_session=db_session, query=sql_query)
        if errors:
            error_message = "\n".join(errors)
            raise Exception(error_message)
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.PREHOOK_SQL_ERROR
        show_error_message(error_prefix.value, suffix)


def alter_column_type(db_session, table_name, column, new_type='TEXT',schema=DESTINATION_SCHEMA.DESTINATION_NAME.value):
    query = f'''ALTER TABLE {schema}.{table_name}
               ALTER COLUMN {column} TYPE {new_type};'''
    execute_query(db_session, query)

def concat_dfs_in_dir(folder_path):
    try:
        dataframes = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(folder_path, filename)
                df = pd.read_csv(file_path)
                dataframes.append(df)
        df_concat = pd.concat(dataframes, ignore_index=True)
        return df_concat
    except:
        return pd.DataFrame()

def return_local_csvs_concated():
    try:
        df_companies = concat_dfs_in_dir('local_csvs/company_info/')
        df_postings = concat_dfs_in_dir('local_csvs/jobs/')
        df_details = concat_dfs_in_dir('local_csvs/job_details/')
        return df_companies, df_postings, df_details
    except:
        return pd.DataFrame(),pd.DataFrame(),pd.DataFrame()

def convert_type_before_hook(df_companies, df_postings, df_details):
    try:
        df_companies['company_id'] =df_companies['company_id'].astype(str)
        df_postings['ID'] =df_postings['ID'].astype(str)
        df_details = df_details.astype({'ID': str, 'company_id': str})
        return df_companies, df_postings, df_details
    except:
        print('error converting')

def prehook_local_files_into_pg(db_session):
    
    df_companies, df_postings, df_details = return_local_csvs_concated()
    df_companies, df_postings, df_details = convert_type_before_hook(df_companies, df_postings, df_details)
    dfs = {'companies': df_companies, 'postings': df_postings, 'details':df_details}    
    for df_name, df in dfs.items():
        print('Doing DF', df_name)
        stmnt = return_create_statement_from_df_stg(df, df_name)
        execute_query(db_session, stmnt)
        queries = return_insert_into_sql_statement_from_df_stg(df, df_name)
        for query in queries:
            execute_query(db_session, query)
        print('DONE DF')

def prehook():

    db_session = create_connection()

    execute_sql_folder(db_session)

    prehook_local_files_into_pg(db_session)