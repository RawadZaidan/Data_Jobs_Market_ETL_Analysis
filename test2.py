from main import job_data_get
from requests_html import HTMLSession

s = HTMLSession()
u = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data%2Bengineer&location=United%2BStates&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&start=0'
resp = s.get(u)
prod = resp.html.xpath('//h3[@class = "base-search-card__title"]')
titles = []
companies = resp.html.xpath('//a[@class = "hidden-nested-link"]')
companies_list = []
for p in prod:
    titles.append(p.text)
for company in companies:
    companies_list.append(company.text)
print(titles)
print(companies_list)