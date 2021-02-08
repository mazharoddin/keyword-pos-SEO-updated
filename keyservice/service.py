import os
import sys
import csv
import ssl
import random
import smtplib
import time
import urllib
import platform
import logging
import urllib.request as req
import urllib.request as urllib2
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from datetime import date
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup

from .models import Position, Keyword, MapPosition

logger = logging.getLogger("django")


def add_log(key):
    msg = "position: {}".format(key)
    logger.info(msg)


def find_keyword(url):
    if "http" in url:
        url = url.split("//")[1]
    else:
        url = url.split("/")[0]
    return Keyword.objects.filter(urls=url).first()


def format_date(data_str):
    data = data_str.split("/")
    return "%s-%s-%s" % (data[2], data[0], data[1])


def handle_uploaded_file(file):
    position_list = []
    keyword = None
    fr = file.read().decode("utf-8")
    lines = fr.split("\n")
    lines.pop(0)
    lines.pop()
    count = 1
    for line in lines:
        fields = line.split(",")
        keyword = find_keyword(fields[1])
        # date = format_date(fields[0])
        date = fields[1]
        pos = Position(
            date=date,
            url=fields[2],
            key=fields[3],
            city=fields[4],
            position=fields[5],
            keyword_id=keyword,
        )
        position_list.append(pos)
    Position.objects.bulk_create(position_list)
    return None

    #
    # for line in lines:
    #     fields = line.split(",")
    #     # keyword = find_keyword(fields[1])
    #     # date = format_date(fields[0])
    #     date = fields[1]
    #     pos = Keyword(
    #         # date=date,
    #         name=fields[2],
    #         key=fields[3],
    #         city=fields[4],
    #         # position=fields[5],
    #         # keyword_id=keyword,
    #     )
    #     position_list.append(pos)
    # Keyword.objects.bulk_create(position_list)

    # for line in lines:
    #     fields = line.split(",")
    #     keyword = find_keyword(fields[1])
    #     # date = format_date(fields[0])
    #     date = fields[1]
    #     pos = Keyword(
    #         # date=date,
    #         name=fields[2],
    #         priority_keyword=fields[3],
    #         main_keyword=fields[4],
    #         # position=fields[5],
    #         # keyword_id=keyword,
    #     )
    #     position_list.append(pos)
    # Keyword.objects.bulk_create(position_list)
    # return None


def google(query):
    links = []
    address = "http://www.google.com/search?gl=us&q=%s&num=20&hl=en&start=0" % (
        urllib.parse.quote_plus(query)
    )
    request = urllib2.Request(
        address,
        None,
        {
            "User-Agent": "Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
        },
    )
    urlfile = urllib2.urlopen(request)
    page = urlfile.read()
    soup = BeautifulSoup(page, "html.parser")
    for li in soup.findAll("div", attrs={"class": "g"}):
        sLink = li.find("a")
        try:
            if sLink["href"] and sLink["href"].startswith("http"):
                links.append(sLink["href"])
        except KeyError:
            print("error")
    return links


def save_detail(file):
    subject = "An email with attachment from DESSS SEO"
    body = "This is an email with attachment sent from DESSS SEO"
    sender_email = "chatbot@desss.com"
    receiver_email = "gopi@desss.com"
    password = "C!!@tb0t"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # message["Bcc"] = ""
    message.attach(MIMEText(body, "plain"))
    filename = file
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename= %s" % filename)
    message.attach(part)
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.ionos.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def callback():
    save_detail(filewrite)


def normalize_url(url):
    if "http" in url:
        url = url.split("//")[1]
    if "wwww" in url:
        url = url.replace("www.", "")
    return url


def normalize_keyword(keyword):
    return keyword.strip()


def normalize_city(city):
    return city.strip()


def get_query(keyword, city):
    keyword = normalize_keyword(keyword)
    city = normalize_city(city)
    query = "{} {}".format(keyword, city)
    # print(query)
    return query


def get_result(url, keyword, city):
    count = 0
    found = 0
    url = normalize_url(url)
    add_log(url)
    query = get_query(keyword, city)
    add_log(query)
    # print(url, keyword, city)
    delay = random.randint(72, 180)
    if found == 0:
        for res in google(query):
            print(res)
            count = count + 1
            # add_log(res)
            if res.find(url) != -1 and found == 0:
                found = count
                add_log(res)
        time.sleep(delay)
    # print(found, count)
    return found


def read_and_process_csv(read_file_csv):
    temp = []
    with open(read_file_csv, "r") as fr:  # open a csv file
        csvdata = csv.reader(fr)
        header = next(csvdata)
        count = len(list(csvdata))
        ex = random.randint(0, count)
        print(header)
        sn = 0
        for row in csvdata:
            if sn == ex:
                sys.exit()
            url = row[1]
            keyword = row[2]
            city = row[3]
            position = get_result(url, keyword, city)
            sn = sn + 1
            today = date.today()
            temp.append([sn, today, url, keyword, city, position])
        return temp


def write_csv(write_file_csv, header, result):
    with open(filewrite, mode="w") as fw:
        csv_write = csv.writer(fw)
        csv_write.writerow(header)
        csv_write.writerows(result)


####################################### MAP #########################################


def create_request(query):
    quote_query = quote_plus(query.strip())
    url = "http://www.google.com/search?gl=us&q=%s&num=20&hl=en&start=0" % (quote_query)
    request = req.Request(
        url,
        None,
        {
            "User-Agent": "Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
        },
    )
    return request


def create_request2(url):
    request = req.Request(
        url,
        None,
        {
            "User-Agent": "Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
        },
    )
    return request


def read_page(request):
    try:
        urlfile = req.urlopen(request)
        page = urlfile.read()
        #    print(page)
        return page
    except:
        print("error in url openning")


def get_soup(page):
    soup = BeautifulSoup(page, "html.parser")
    return soup


def check_is_map(soup):
    return soup.find("div", class_="xERobd")


def process_page(soup):
    sleep_time = random.randint(16, 33)
    result_list = list()
    links = soup.find_all("div", class_="dbg0pd")
    for link in links:
        result_list.append(link.text)
    time.sleep(sleep_time)
    return result_list


def get_next_page(base_url, soup):
    print("get next page")
    sleep_time = random.randint(58, 78)
    link = soup.find("a", class_="Q2MMlc")
    # href next page link is changed
    # get_href = soup.find("div", class_="xERobd")
    # link = get_href.a
    if link is None:
        return None
    next_page = link["href"]
    url = base_url + next_page
    print(url)
    #    url="https://www.google.com/search?num=20&hl=en&q=hospital&npsic=0&rflfq=1&rldoc=1&rlha=0&rllag=11666405,78143670,342&tbm=lcl&sa=X&ved=2ahUKEwj5-encxOjpAhVlwTgGHZ4RAgIQjGp6BAgWEDo"
    request = create_request2(url)
    page = read_page(request)
    time.sleep(sleep_time)
    return page


def get_map_result(name, key, city):
    print(name)
    found, count = 0, 0
    query = key + " " + city
    # query = "hospital"
    base_url = "https://www.google.com"

    request = create_request(query)
    page = read_page(request)
    sleep_time = random.randint(36, 58)
    soup = get_soup(page)
    check_map = check_is_map(soup)
    # print(check_map)
    try:
        if check_map is not None:
            time.sleep(sleep_time)
            map_page = get_next_page(base_url, soup)
            if map_page is None:
                return found
            map_soup = get_soup(map_page)
            site_names = process_page(map_soup)
            for site_name in site_names:
                # print("...................")
                # print(site_name)
                count += 1
                for names in name.split(","):
                    print(names)
                    if site_name.find(names) != -1 and found == 0:
                        found = count
            return found
        else:
            return found
    except Exception:
        return found

def get_map_results(name, key, city):
    print(name)
    res=list()
    found, count = 0, 0
    query = key + " " + city
    # query = "hospital"
    base_url = "https://www.google.com"

    request = create_request(query)
    page = read_page(request)
    sleep_time = random.randint(36, 58)
    soup = get_soup(page)
    check_map = check_is_map(soup)
    # print(check_map)
    try:
        if check_map is not None:
            time.sleep(sleep_time)
            map_page = get_next_page(base_url, soup)
            if map_page is None:
                return found
            map_soup = get_soup(map_page)
            site_names = process_page(map_soup)
            for site_name in site_names:
                # print("...................")
                # print(site_name)
                count += 1
                for names in name.split(","):
                    print(names)
                    if site_name.find(names) != -1 and found == 0:
                        found = count
                res.append(found)
            return res
        else:
            return res
    except Exception:
        return res


if __name__ == "__main__":
    fileread = "txgidoc.csv"
    filewrite = "txgidoc-report.csv"
    fields = ["SNo", "Date", "Url", "Keyword", "City", "Position"]
    result = read_and_process_csv(fileread)
    write_csv(filewrite, fields, result)
    if platform.system().lower() == "window":
        os.system("attrib +r " + filewrite)
    callback()

    # For Map process checking
    # res = get_map_result("test", "test", "test")
    # print()
    # print(res)

def map_upload(file):
    position_list = []
    keyword = None
    fr = file.read().decode("utf-8")
    lines = fr.split("\n")
    lines.pop(0)
    lines.pop()
    count = 1
    for line in lines:
        fields = line.split(",")
        # keyword = find_keyword(fields[3])
        # date = format_date(fields[0])
        date = fields[1]
        pos = MapPosition(
            # date=date,
            name=fields[2],
            key=fields[3],
            city=fields[4],
            position=fields[5],
            # keyword_id=keyword,
        )
        position_list.append(pos)
    MapPosition.objects.bulk_create(position_list)
    return None
