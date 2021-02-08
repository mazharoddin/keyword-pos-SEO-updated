import os
import csv
import logging
from datetime import date, datetime, timedelta
from .models import Keyword, City, Position, MapPosition, KeywordCityRel
from .service import get_result, get_map_result,get_map_results, handle_uploaded_file, map_upload, google

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PAR_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir))

logger = logging.getLogger("django")


def _check_and_convert_position(pos):
    # msg = "position: {}".format(pos)
    # logger.info(msg)
    if pos == 0:
        pos = 21
    return pos


def _get_record(seq, url, key, city, keyword):
    pos = _check_and_convert_position(get_result(url, key, city))
    return Position(seq_no=seq, url=url, key=key, city=city, position=pos, keyword_id=keyword)


def _check_record(url, key, city):
    if not len(key.strip()) > 0:
        return True
    yesterday = date.today() - timedelta(days=2)
    status = Position.objects.filter(url=url, key=key, city=city, date__gte=yesterday).exists()
    return status


def _get_map_record(seq, name, key, city, keyword):
    if(len(name.split(","))>1):
        i=0
        records=list()
        positions=get_map_results(name,key,city)
        for site in name.split(","):
           try:
                pos= _check_and_convert_position(positions[i])
           except:
                pos=21
           record=MapPosition(seq_no=seq, name=site, key=key, city=city, position=pos, keyword_id=keyword)
           records.append(record)
           i+=1
        return records
    else:    
        pos = _check_and_convert_position(get_map_result(name, key, city))
        return MapPosition(seq_no=seq, name=name, key=key, city=city, position=pos, keyword_id=keyword)


def _check_map_record(name, key, city):
    # print(name, key, city)
    if not len(key.strip()) > 0:
        return True
    return MapPosition.objects.filter(name=name.split(",")[0], key=key, city=city, date=date.today()).exists()


def _get_search_records(site, date):
    fileds = ["S.No", "Date", "Url", "Keyword", "City", "Position"]
    positions = (
        Position.objects.filter(date__year=date.year)
        .filter(date__month=date.month)
        .filter(keyword_id=site.id)
    )

    with open("position.csv", mode="w") as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow(fileds)
        for position in positions:
            csv_write.writerow(
                [
                    position.seq_no,
                    position.date,
                    position.url,
                    position.key,
                    position.city,
                    position.position,
                ]
            )
    filepath = os.path.join(PAR_DIR, "position.csv")
    return filepath


def _get_map_records(site, date):
    fileds = ["S.No", "Date", "Name", "Keyword", "City", "Position"]
    positions = (
        MapPosition.objects.filter(date__year=date.year)
        .filter(date__month=date.month)
        .filter(keyword_id=site.id)
    )

    with open("position.csv", mode="w") as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow(fileds)
        for position in positions:
            csv_write.writerow(
                [
                    position.seq_no,
                    position.date,
                    position.name,
                    position.key,
                    position.city,
                    position.position,
                ]
            )
    filepath = os.path.join(PAR_DIR, "position.csv")
    return filepath


def _get_graph_record(site, start_month, start_year, end_month, end_year):
    fileds = ["S.No", "Date", "Url", "Keyword", "City", "Position"]
    positions = (
        Position.objects.filter(date__year__gte=int(start_year))
        .filter(date__month__gte=int(start_month))
        .filter(keyword_id=site.id)
        .order_by("date")
    )
    write_path = os.path.join("graph", "graph_position.csv")
    with open("graph_position.csv", mode="w") as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow(fileds)
        for position in positions:
            csv_write.writerow(
                [
                    # position.seq_no,
                    position.date,
                    position.url,
                    position.key,
                    position.city,
                    position.position,
                ]
            )


def _keywords_to_positions(keys, secondary_keywords, cities, keyword):
    all_pos, temp, seq, = list(), list(), 0
    url = keyword.urls
    keywordcitys = KeywordCityRel.objects.filter(keyword_id=keyword.id)
    for m_keyword in keys:
        for s_keyword in secondary_keywords:
            seq += 1
            if s_keyword is ".":
                s_keyword = " "
            both_key = m_keyword + " " + s_keyword
            if cities.exists():
                for city in cities:
                    if not _check_record(url, both_key, city.name):
                        data = _get_record(seq, url, both_key, city.name, keyword)
                        temp.append(data)
                        data.save()
                all_pos = all_pos + temp
                temp = []
            elif keywordcitys.exists():
                for keywordcity in keywordcitys:
                    record_exist = _check_record(url, both_key, keywordcity.city_id.name)
                    print(url, both_key, keywordcity.city_id.name, record_exist)
                    if not record_exist:
                        data = _get_record(seq, url, both_key, keywordcity.city_id.name, keyword)
                        temp.append(data)
                        data.save()
                all_pos = all_pos + temp
                temp = []
            else:
                if not _check_record(url, both_key, ""):
                    print(url, both_key, "..")
                    data = _get_record(seq, url, both_key, "", keyword,)
                    print(data)
                    temp.append(data)
                    data.save()
                all_pos = all_pos + temp
                temp = []
    return all_pos
