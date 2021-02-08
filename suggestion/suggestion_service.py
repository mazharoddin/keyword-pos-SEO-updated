import time
import random
import urllib.request as req
from urllib.parse import quote
from bs4 import BeautifulSoup


def create_request(query):
    quote_query = quote(query)
    url = "https://www.google.com/search?q=%s&num=20&hl=en&start=0" % (quote_query)
    request = req.Request(
        url,
        None,
        {
            "User-Agent": "Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
        },
    )
    return request


def read_page(request):
    urlfile = req.urlopen(request)
    page = urlfile.read()
    return page


def get_soup(page):
    soup = BeautifulSoup(page, "html.parser")
    return soup


def check_is_suggestion(soup):
    return soup.find("div", id="extrares")


def check_is_inner_suggestion(soup):
    return soup.find("div", class_="UUbT9")


def process_suggestions(soup):
    sugg_list = list()
    links = soup.find_all("p", class_="nVcaUb")
    for link in links:
        sugg_list.append(link.text)
    return sugg_list


def process_inner_suggestions(soup):
    links = soup.find_all("div", class_="sbl1")
    for link in links:
        print(link.text)


def get_suggestion(keyword):
    sleep_time = random.randint(45, 72)
    suggestion_list = list()
    # query = "books"
    query = keyword
    request = create_request(query)
    page = read_page(request)
    soup = get_soup(page)
    sugg = check_is_suggestion(soup)
    if sugg is not None:
        suggestion_list = process_suggestions(soup)
    time.sleep(sleep_time)
    return suggestion_list
