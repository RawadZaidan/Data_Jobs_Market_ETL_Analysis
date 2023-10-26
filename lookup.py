from enum import Enum

#--------------- Data Base ---------------#

class ErrorHandling(Enum):
    DB_CONNECT_ERROR = "DB Connect Error"
    DB_RETURN_QUERY_ERROR = "DB Return Query Error"
    API_ERROR = "Error calling API"
    RETURN_DATA_CSV_ERROR = "Error returning CSV"
    RETURN_DATA_EXCEL_ERROR = "Error returning Excel"
    RETURN_DATA_SQL_ERROR = "Error returning SQL"
    RETURN_DATA_UNDEFINED_ERROR = "Cannot find File type"
    EXECUTE_QUERY_ERROR = "Error executing the query"
    NO_ERROR = "No Errors"
    PREHOOK_SQL_ERROR = "Prehook: SQL Error"
    PREHOOK_CLOSE_CONNECTION_ERROR = "Error closing connection"
    HOOK_DICT_RETURN_ERROR = "Error returning lookup items as dict"
    DB_RETURN_INSERT_INTO_SQL_STMT_ERROR = "Return insert into sql dataframe error:"
    CSV_ERROR = "Error importing csv files from path"
    PANDAS_NULLS_ERROR = "Error dropping nulls from df"
    PANDAS_FILL_NULLS_ERROR="Error replacing nulls from df"
    IMPORTING_LOCAL_CSVS_INTO_PG_ERROR = "Error importing local csvs into postgres"
    REMOVING_SPACES_COLUMN_ERROR = "Error removing spaces from column names df - Hook-Pre.py"
    CLEANING_CSVS_BEFORE_PG_ERROR = "Error cleaninig csvs before migration"
    LINKEDIN_COMPANY_INFO_ERROR = "Error getting company info"
    LINKEDIN_INDIVIDUAL_JOBS_ERROR = "Error getting individual jobs"
    SELENIUM_DRIVER_ERROR = "Error starting selenium driver"
    QUIT_DRIVER_ERROR = "Error quitting driver"
    GLASSDOOR_COMPANIES_ERROR = "Error getting company info from glassdoor"
    GLASSDOOR_INDIVIDUALS_ERROR = "Error getting individual jobs"
    GLASSDOOR_POSTINGS_ERROR = "Error getting postings from Glassdoor"
    GLASSDOOR_FETCH_POSTINGS_ERROR = "Error fetching postings"
    GLASSDOOR_CLEANING_POSTINGS_ERROR = "Error cleaning postings"
    NAKURI_GET_DETAILS_ERROR = "Error fetching Nakuri jobs details"
    NAKURI_GET_ALL_POSTINGS_ERROR = "Error getting all postings"
    NAKURI_GET_ALL_POSTINGS_ONEPAGE_ERROR = "Error fetching all the data on one page"
    NAKURI_GET_JOBS_ERROR = "Error getting info from individual jobs"
    NAKURI_GET_DATE_ERROR = "Error getting date"
    
class InputTypes(Enum):
    SQL = "SQL"
    CSV = "CSV"
    EXCEL = "Excel"

class DESTINATION_SCHEMA(Enum):
    DESTINATION_NAME = "stg_jobs_db"

class AllStagingTables(Enum):
    tables = ['companies', 'comparison', 'details', 'geomap_interest', 'postings']

#--------------- LOCAL PATHS ---------------#

class CSV_FOLDER_PATH(Enum):
    prehook_csvs = 'csvs'

class SQL_PREHOOK_COMMANDS_PATH(Enum):
    path = 'sql_commands'

#--------------- Glassdoor ---------------#

class glassdoor(Enum):
    link = 'https://www.glassdoor.com/Job/data-engineer-jobs-SRCH_KO0,13.htm?fromAge=1'

class glassdoor_xpaths(Enum):
    XPATH_NUMBER_OF_ELEMENTS = '//*[@id="left-column"]/div[1]/h1'
    XPATH_NEXT_PAGE = '//*[@id="left-column"]/div[2]/div/button'
    XPATH_EXIT_LOGIN = '/html/body/div[11]/div[2]/div[1]/button'
    
class glassdoor_classes(Enum):
    CLASS_JOB_TITLE        = 'JobCard_seoLink__r4HUE'
    CLASS_JOB_LOCATION     = 'JobCard_location__DX0MJ'
    CLASS_JOB_COMPANY_NAME = 'EmployerProfile_profileContainer__nonKT'
    CLASS_JOB_SALARY       = 'JobCard_salaryEstimate__TLvO7'
    CLASS_JOB_DATE         = 'd-flex'

class ORDERED_DF(Enum):
    list_ordered_columns = ['ID', 'title', 'company', 'location', 'posting_date', 'link', 'source']

class TAGS(Enum):
    LI = 'li'

# class GLASSDOOR_DF(Enum):
#     BOARD_COLUMNS_LIST = ['title','company','location','link','salary']

class glassdoor_css_selectors(Enum):
    LI_JOBS_LIST = 'li.JobsList_jobListItem__JBBUV'
    LI_JOB_DATE = '[data-test="job-age"]'

#--------------- LinkedIn ---------------#

class linkedin_xpaths(Enum):
    JOB_TITLE = '//h3[@class = "base-search-card__title"]'
    COMPANIES = '//a[@class = "hidden-nested-link"]'
    LINKS = '//a[@class = "base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"]'
    POSTING_TIME = '//time[@class = "job-search-card__listdate"]'
    LOCATIONS = '//span[@class = "job-search-card__location"]'

class linkedin_attributes(Enum):
    HREF = 'href'
    DATETIME = 'datetime'

class LINKEDIN_DF_COLUMNS(Enum):
        COLUMNS_LIST = ['title','company','location','link','posting_date']

class linkedin_url(Enum):
    url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%2BAnalyst&location=Worldwide&locationId=&geoId=92000000&f_TPR=r86400&start='

#--------------- Nakuri ---------------#

class nakuri_url(Enum):
    url = 'https://www.naukrigulf.com/data-engineer-jobs-?sort=date'