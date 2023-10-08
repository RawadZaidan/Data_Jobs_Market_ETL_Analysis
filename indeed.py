from requests_html import HTMLSession
from time import sleep

def get_data(session, url):
    r = session.get(url, verify=False)
    sleep(2)
    return r.html.find('div.job_seen_beacon')

def parse_html (html):
    pass
    # job = {
    # 'title': html.find('h2> a')[0].text,
    # I
    # }
    # return job
def main():
    session = HTMLSession()
    url = 'https://uk.indeed.com/jobs?q-python%20developer&l=bristol'
    jobs = get_data(session, url)
    # for job in jobs:
    #     print(parse_html (job))

if __name__ == '__main__':
    main()  