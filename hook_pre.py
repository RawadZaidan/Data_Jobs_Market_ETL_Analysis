from database_handler import execute_query, create_connection,return_create_statement_from_df
from lookup import ErrorHandling, InputTypes, DESTINATION_SCHEMA, SQL_COMMANDS_PATH
from database_handler import return_insert_into_sql_statement_from_df
from logging_handler import show_error_message
from lookup import DRIVE_CSVS
import pandas as pd
import datetime
import logging
import os

def logging_main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",  # Fix the typo here
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="log.txt"
    )

def concat_dfs(*dfs):
    df_concatenated = pd.concat(dfs, ignore_index=True)
    return df_concatenated

def read_csv_files_from_github(url):
    df = pd.read_csv(url)
    return df

def remove_spaces_from_columns_df(df):
    try:
        for column in df.columns:
            new_column_name = column.replace(' ', '_')
            df.rename(columns={column: new_column_name}, inplace=True)
        return df
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.REMOVING_SPACES_COLUMN_ERROR.value
        show_error_message(error_prefix, suffix)

def execute_sql_folder(db_session, sql_command_directory_path=SQL_COMMANDS_PATH.path.value):
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

def comparison_df_transform_salary(s):
    try:
        x = int(str(s)[1:-1])*1000
        return x
    except:
        pass

def concat_dfs(*args):
    try:
        df_concatenated = pd.concat(args, ignore_index=True)
        return df_concatenated
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.CONCAT_DFS_ERROR
        show_error_message(error_prefix.value, suffix)

def read_geomap_df_from_drive():
    try:
        list_of_csvs = DRIVE_CSVS.geomap.value
        df1 = read_csv_files_from_github(list_of_csvs[0])
        df2 = read_csv_files_from_github(list_of_csvs[1])
        df3 = read_csv_files_from_github(list_of_csvs[2])

        df_merged = df1.merge(df2, on='Country',how='outer').merge(df3, on='Country',how='outer')
        df_merged.fillna(0, inplace=True)
        return df_merged
    except:
        return pd.DataFrame()

def fix_posting_date(date):
    try:
        sliced_date = date.split('-')
        if int(sliced_date[0]) > 2000:
            new_date = date
        else:
            new_date = sliced_date[1]+'-'+sliced_date[2]+'-'+sliced_date[0]
        return new_date
    except:
        print('error fixing date in fix_posting_date function')

def return_concatenated_df_from_drive(lookup_list_of_urls): 
    dfs = []
    for link in lookup_list_of_urls:
        df = read_csv_files_from_github(link)
        dfs.append(df)
    final = pd.concat(dfs, ignore_index=True)
    return final 

def return_local_csvs_concated():
    try:
        df_companies = return_concatenated_df_from_drive(DRIVE_CSVS.company_info.value)
        df_postings = return_concatenated_df_from_drive(DRIVE_CSVS.postings.value)
        df_details = return_concatenated_df_from_drive(DRIVE_CSVS.job_details.value)
        df_comparison = return_concatenated_df_from_drive(DRIVE_CSVS.comparison.value)
        df_interest_timeline = return_concatenated_df_from_drive(DRIVE_CSVS.interest_timeline.value)
        return df_companies, df_postings, df_details, df_comparison,df_interest_timeline
    except:
        return pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()

def clean_before_hook(df_companies, df_postings, df_details, df_comparison):
    try:
        df_companies['company_id'] =df_companies['company_id'].astype(str)
        df_postings['ID'] =df_postings['ID'].astype(str)
        df_postings['posting_date'] = df_postings['posting_date'].apply(lambda x: x.replace('/', '-'))
        df_postings['posting_date'] = df_postings['posting_date'].apply(fix_posting_date)
        df_details = df_details.astype({'ID': str, 'company_id': str})
        df_comparison['Lower_Salary'] = df_comparison['Lower_Salary'].apply(comparison_df_transform_salary)
        df_comparison['Higher_Salary'] = df_comparison['Higher_Salary'].apply(comparison_df_transform_salary)
        df_comparison = remove_spaces_from_columns_df(df_comparison)
        return df_companies, df_postings, df_details, df_comparison
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.CLEANING_CSVS_BEFORE_PG_ERROR.value
        show_error_message(error_prefix, suffix)

def prehook_local_files_into_pg(db_session):
    try:
        df_companies, df_postings, df_details, df_comparison,df_interest_timeline = return_local_csvs_concated()
        df_companies, df_postings, df_details, df_comparison = clean_before_hook(df_companies, df_postings, df_details, df_comparison)
        df_geomap = read_geomap_df_from_drive()
        dfs = {'companies': df_companies, 'postings': df_postings, 'details':df_details,
            'comparison':df_comparison, 'geomap_interest':df_geomap, 'comparison_timeline': df_interest_timeline}    
        for df_name, df in dfs.items():
            stmnt = return_create_statement_from_df(dataframe=df,prefix='stg_', table_name=df_name)
            execute_query(db_session, stmnt)
            queries = return_insert_into_sql_statement_from_df(dataframe=df, table_name=df_name,prefix='stg_')
            for query in queries:
                execute_query(db_session, query)
            logging.info(f'Pre_Hook: Df:{df_name} is done.')
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.IMPORTING_LOCAL_CSVS_INTO_PG_ERROR.value
        show_error_message(error_prefix, suffix)

def prehook():

    db_session = create_connection()

    execute_sql_folder(db_session)
    logging.info('Pre_Hook: SQL folder executed')

    prehook_local_files_into_pg(db_session)
    logging.info('Pre_Hook: CSVs read and uploaded to database')