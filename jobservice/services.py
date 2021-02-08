import requests
from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup


def download_page(url):
    res = urlopen(url).read()
    return res


def download_page1(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.text
    else:
        return None


def process_page(page):
    res = list()
    soup = BeautifulSoup(page, "html.parser")
    soup.prettify()
    group = soup.find(id="resultsCol")
    job_cards = group.find_all(class_="jobsearch-SerpJobCard")
    for job in job_cards:
        title = job.find(class_="jobtitle").text.strip()
        location = job.find(class_="location").text.strip()
        summary = job.find(class_="summary").text.strip()
        url_suffix = job.find("a", class_="jobtitle", href=True).get("href")
        url = "https://www.indeed.com" + url_suffix
        res.append([title, location, summary, url])
    return res


def get_job_details(job, location):
    url = "https://www.indeed.com/jobs?q={}&l={}".format(
        quote_plus(job), quote_plus(location)
    )
    page = download_page1(url)
    if page:
        return process_page(page)
    return None


if __name__ == "__main__":
    job = "Hybris"
    location = "Austin,TX"
    url = "https://www.indeed.com/jobs?q={}&l={}".format(
        quote_plus(job), quote_plus(location)
    )
    page = download_page1(url)
    if page:
        result = process_page(page)
        print(result)
    print("END")
