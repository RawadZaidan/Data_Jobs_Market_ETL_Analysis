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
    RETURN_NET_TRASNFER_ERROR = "Error handling net transfer fee"
    PLAYERS_ERROR = "Error cleaning players csv"
    PLAYERVALUATIONS_ERROR = "Error cleaning player valuations csv"
    GAMES_ERROR = "Error cleaning games csv"
    GAMES_EVENTS_ERROR = "Error cleaning games events csv"
    COMPETITIONS_ERROR = "Error cleaning competitions csv"
    CLUBS_ERROR = "Error cleaning clubs csv"
    APPEARANCES_ERROR = "Error cleaning appearances csv"

class InputTypes(Enum):
    SQL = "SQL"
    CSV = "CSV"
    EXCEL = "Excel"

class DESTINATION_SCHEMA(Enum):
    DESTINATION_NAME = "jobs_db"

#--------------- Glassdoor ---------------#

class glassdoor(Enum):
    link = 'https://www.glassdoor.com/Job/data-engineer-jobs-SRCH_KO0,13.htm?fromAge=3'

class glassdoor_xpaths(Enum):
    XPATH_NUMBER_OF_ELEMENTS = '//*[@id="left-column"]/div[1]/h1'
    XPATH_NEXT_PAGE = '//*[@id="left-column"]/div[2]/div/button'
    XPATH_EXIT_LOGIN = '/html/body/div[11]/div[2]/div[1]/button'
    
class glassdoor_classes(Enum):
    CLASS_JOB_TITLE        = 'css-1nh9iuj'
    CLASS_JOB_LOCATION     = 'location'
    CLASS_JOB_COMPANY_NAME = 'css-8wag7x'
    CLASS_JOB_SALARY       = 'salary-estimate'
    CLASS_JOB_DATE         = 'd-flex'

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
    url = 'https://www.naukrigulf.com/data-engineer-jobs-'