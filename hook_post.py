from database_handler import create_connection, execute_query
from lookup import AllStagingTables

def truncate_all_staging_tables(db_session):
    for table in AllStagingTables.tables.value:
        try:
            query = f'TRUNCATE TABLE stg_jobs_db.stg_{table}'
            execute_query(db_session,query)
        except:
            print('Error Truncating')

def post_hook():

    db_session = create_connection()

    truncate_all_staging_tables(db_session)