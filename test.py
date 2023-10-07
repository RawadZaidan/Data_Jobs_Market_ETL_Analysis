from main import job_data_get
from requests_html import HTMLSession

s = HTMLSession()
u = 'https://www.linkedin.com/jobs/search?keywords=data%20engineer&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
resp = s.get(u)
prod = resp.html.xpath('//ul[@class = "jobs-search__results-list"]')
for p in prod:
    print(p.text)