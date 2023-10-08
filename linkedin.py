from main import job_data_get
from requests_html import HTMLSession
from time import sleep

s = HTMLSession()
u = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data%2Bengineer&location=United%2BStates&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&start=0'
resp = s.get(u)

title = resp.html.xpath('//h3[@class = "base-search-card__title"]')
titles = []
companies = resp.html.xpath('//a[@class = "hidden-nested-link"]')
companies_list = []
links = resp.html.xpath('//a[@class = "base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"]')
links_list = []
times = resp.html.xpath('//time[@class = "job-search-card__listdate"]')
times_list = []
locations = resp.html.xpath('//span[@class = "job-search-card__location"]')
locations_list = []
for t in title:
    titles.append(t.text)
for company in companies:
    companies_list.append(company.text)
for link in links:
    links_list.append(link.attrs['href'])
for time in times:
    times_list.append(time.attrs['datetime'])
for location in locations:
    locations_list.append(location.text)
print(titles)
print(companies_list)
print(links_list)
print(times_list)
print(locations_list)