from ws import linkedin_final_df, linkedin_individual_iterate_and_get_df,linkedin_get_company_info, selenium_driver
from database_handler import return_create_statement_from_df_stg,return_insert_into_sql_statement_from_df_stg
from ws import glassdoor_final_df, glassdoor_ind_jobs_df, glassdoor_companies_info_df
from hook_pre import comparison_df_transform_salary,remove_spaces_from_columns_df
from database_handler import create_connection, return_data_as_df
from ws import nakuri_get_all_postings,  nakuri_get_job_details
from logging_handler import show_error_message
from lookup import InputTypes, ErrorHandling
from database_handler import execute_query
from datetime import date
import pandas as pd
import datetime
import os

def return_etl_last_updated_date(db_session):
    execute_hook = False
    query = "SELECT * FROM stg_jobs_db.etl_checkpoint ORDER BY last_etl_date DESC LIMIT 1"
    etl_df = return_data_as_df(
        file_executor= query,
        input_type= InputTypes.SQL,
        db_session= db_session
    )
    if len(etl_df) == 0:
        # choose oldest day possible AKA Zahi's Birthday:p 
        return_date = datetime.date(1992,6,19)
    else:
        return_date = etl_df['last_etl_date'].iloc[0]
    today = datetime.date.today()
    if return_date < today:
        execute_hook = True
    return today, execute_hook

def execute_sql_folder(db_session, sql_command_directory_path='sql_commands_hook'):
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

#-----------------------------------------------------------#

def get_all_new_data():

    print('Waitng for driver...')
    driver = selenium_driver()

    linkedin_postings = linkedin_final_df()
    glassdoor_postings = glassdoor_final_df(driver)
    naukri_postings = nakuri_get_all_postings(driver)

    linkedin_ind = linkedin_individual_iterate_and_get_df(linkedin_postings)
    glassdoor_ind = glassdoor_ind_jobs_df(driver, glassdoor_postings)
    naukri_ind = nakuri_get_job_details(naukri_postings,driver)

    linkedin_company = linkedin_get_company_info(linkedin_ind)
    glassdoor_company = glassdoor_companies_info_df(driver, glassdoor_ind)

    df_postings   = pd.concat([linkedin_postings,glassdoor_postings,naukri_postings], ignore_index=True)
    df_details    = pd.concat([linkedin_ind,glassdoor_ind,naukri_ind], ignore_index=True)
    df_companies  = pd.concat([linkedin_company,glassdoor_company], ignore_index=True)

    return df_companies, df_postings, df_details

def clean_for_hook(df_companies, df_postings, df_details):
    try:
        df_companies['company_id'] =df_companies['company_id'].astype(str)
        df_postings['ID'] =df_postings['ID'].astype(str)
        df_details = df_details.astype({'ID': str, 'company_id': str})
        return df_companies, df_postings, df_details
    except:
        print('error converting')

def get_clean_new_data():
    try:
        df_companies, df_postings, df_details = get_all_new_data()
        df_companies, df_postings, df_details = clean_for_hook(df_companies, df_postings, df_details)
        return df_companies, df_postings, df_details
    except Exception as e:
        print(Exception)

def upload_dfs_into_pg(db_session):
    df_companies, df_postings, df_details = get_clean_new_data()
    dfs = {'companies': df_companies, 'postings': df_postings, 'details':df_details}    
    for df_name, df in dfs.items():
        print('Doing DF', df_name)
        stmnt = return_create_statement_from_df_stg(df, df_name)
        execute_query(db_session, stmnt)
        queries = return_insert_into_sql_statement_from_df_stg(df, df_name)
        for query in queries:
            execute_query(db_session, query)
        print('DONE DF')

def update_etl(db_session, date):
    try:
        query = 'TRUNCATE TABLE stg_jobs_db.etl_checkpoint'
        execute_query(db_session, query)
        query = f"INSERT INTO stg_jobs_db.etl_checkpoint (last_etl_date) VALUES ('{date}')"
        execute_query(db_session, query)
    except:
        print('error')

def upload_after_etl_check(db_session):

    date, check = return_etl_last_updated_date(db_session)
    print(date, check)
    if check:
        update_etl(db_session, date)
        print('UPDATED ETL')
        upload_dfs_into_pg(db_session)
        print('DONE WITH DFS')
        execute_sql_folder(db_session)
        print('EXECUTED SQL')

def execute_sql_folder(db_session, sql_command_directory_path='sql_commands_hook'):
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
#-----------------------------------------------------------#
# Final steps: piecing everything together

def hook():

    db_session = create_connection()

    upload_after_etl_check(db_session)