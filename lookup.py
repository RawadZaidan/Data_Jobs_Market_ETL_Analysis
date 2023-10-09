from enum import Enum

class glassdoor(Enum):
    link = 'https://www.glassdoor.com/Job/data-engineer-jobs-SRCH_KO0,13.htm?fromAge=7'

class glassdoor_xpaths(Enum):
    XPATH_NUMBER_OF_ELEMENTS = '//*[@id="left-column"]/div[1]/h1'
    
class glassdoor_classes(Enum):
    CLASS_JOB_TITLE        = 'css-1nh9iuj'
    CLASS_JOB_LOCATION     = 'location'
    CLASS_JOB_COMPANY_NAME = 'css-8wag7x'
    CLASS_JOB_SALARY       = 'salary-estimate'
    CLASS_JOB_DATE         = 'd-flex'

class TAGS(Enum):
    LI = 'li'

class GLASSDOOR_DF(Enum):
    BOARD_COLUMNS_LIST = ['title','company','location','link','salary']

class glassdoor_css_selectors(Enum):
    LI_JOBS_LIST = 'li.JobsList_jobListItem__JBBUV'
    LI_JOB_DATE = '[data-test="job-age"]'