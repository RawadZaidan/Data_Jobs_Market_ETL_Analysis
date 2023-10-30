from database_handler import create_connection, execute_query
from lookup import AllStagingTables
import logging

def logging_main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="log.txt"
    )

def truncate_all_staging_tables(db_session):
    for table in AllStagingTables.tables.value:
        try:
            query = f'TRUNCATE TABLE dw_reporting.stg_{table}'
            execute_query(db_session,query)
        except:
            print('Error Truncating')

def post_hook():

    db_session = create_connection()

    truncate_all_staging_tables(db_session)

    logging.info('Post_Hook: Done')