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
import logging
import os

def logging_main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",  # Fix the typo here
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="log.txt"
    )
    # Samples:
    # logging.debug('This is a debug message.')
    # logging.info('This is an info message')
    # logging.critical("This is a critical message")

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

    logging_main()

    driver = selenium_driver()
    logging.info('This is an info message: Hook - Getting Linkedin Postings')
    linkedin_postings = linkedin_final_df()
    logging.info('This is an info message: Hook - DONE Getting Linkedin Postings')
    logging.info('This is an info message: Hook - Getting Glassdoor Postings')
    glassdoor_postings = glassdoor_final_df(driver)
    logging.info('This is an info message: Hook - DONE Getting Glassdoor Postings')
    logging.info('This is an info message: Hook - Getting Naukri Postings')
    naukri_postings = nakuri_get_all_postings(driver)
    logging.info('This is an info message: Hook - DONE Getting Glassdoor Postings')

    logging.info('This is an info message: Hook - Getting Linkedin Job Details')
    linkedin_ind = linkedin_individual_iterate_and_get_df(linkedin_postings)
    logging.info('This is an info message: Hook - DONE Getting Linkedin Job Details')
    logging.info('This is an info message: Hook - Getting Glassdoor Job Details')
    glassdoor_ind = glassdoor_ind_jobs_df(driver, glassdoor_postings)
    logging.info('This is an info message: Hook - DONE Getting Linkedin Job Details')
    logging.info('This is an info message: Hook - Getting Glassdoor Job Details')
    naukri_ind = nakuri_get_job_details(naukri_postings,driver)
    logging.info('This is an info message: Hook - DONE Getting Linkedin Job Details')

    logging.info('This is an info message: Hook - Getting Linkedin Company Details')
    linkedin_company = linkedin_get_company_info(linkedin_ind)
    logging.info('This is an info message: Hook - DONE Getting Linkedin Company Details')
    logging.info('This is an info message: Hook - Getting Glassdoor Company Details')
    glassdoor_company = glassdoor_companies_info_df(driver, glassdoor_ind)
    logging.info('This is an info message: Hook - DONE Getting Glassdoor Company Details')

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
        logging_main()
        df_companies, df_postings, df_details = get_all_new_data()
        logging.info('This is an info message: Hook - Got all Dfs of today')
        df_companies, df_postings, df_details = clean_for_hook(df_companies, df_postings, df_details)
        logging.info('This is an info message: Hook - Cleaned Dfs of today')
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
    logging_main()
    try:
        query = 'TRUNCATE TABLE stg_jobs_db.etl_checkpoint'
        execute_query(db_session, query)
        query = f"INSERT INTO stg_jobs_db.etl_checkpoint (last_etl_date) VALUES ('{date}')"
        execute_query(db_session, query)
    except:
        print('error')
        logging.critical("This is a critical message: Hook - Error updating etl last_run_date")

def upload_after_etl_check(db_session):
    logging_main()
    date, check = return_etl_last_updated_date(db_session)
    execute_sql_folder(db_session)
    if check:
        update_etl(db_session, date)
        logging.info('This is an info message: ETL last_update UPDATED')
        upload_dfs_into_pg(db_session)
        logging.info('This is an info message:Uploaded dataframes into pgadmin')
        execute_sql_folder(db_session)
        logging.info('This is an info message: SQL folder executed')

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
        error_prefix = ErrorHandling.PREHOOK_SQL_ERROR.value
        show_error_message(error_prefix, suffix)
#-----------------------------------------------------------#
# Final steps: piecing everything together

def hook():
    try:
        logging_main()

        db_session = create_connection()
        logging.info('This is an info message: Hook - Created DB_SESSION')

        upload_after_etl_check(db_session)
        logging.info('This is an info message: Hook - Done')
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.HOOK_ERROR.value
        show_error_message(error_prefix.value, suffix)