import os
import csv
import time
import random
from datetime import date, datetime, timedelta
from django.shortcuts import render
from django.views.static import serve
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .models import Keyword, City, Position, MapPosition, KeywordCityRel
from .service import get_result, get_map_result, handle_uploaded_file, map_upload, google
from .graph_report import generate_graph
from .forms import (
    UploadFileForm,
    KeywordToUrlFrom,
    SearchForm,
    MapSearchForm,
    ReportForm,
    GraphReportForm,
)
from .utils import (
    _keywords_to_positions,
    _get_graph_record,
    _get_map_records,
    _get_map_record,
    _get_record,
    _get_search_records,
    _check_map_record,
)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PAR_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir))


def index(request, *args, **kwargs):
    positions = Position.objects.filter(date=date.today())
    if positions is not None and positions.count() != 0:
        # print(positions)
        return render(request, "keyservice/index.html", {"positions": positions, "status": True})
    else:
        return render(request, "keyservice/index.html", {})


def get_position(request, *args, **kwargs):
    all_pos, error = [], ""
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data["site"]
            cities = form.cleaned_data["cities"]

            priority_keyword = keyword.priority_keyword.split(",")
            main_keyword = (
                keyword.main_keyword.split(",") if len(keyword.main_keyword.strip()) > 0 else []
            )
            secondary_keywords = keyword.secondary_keyword.split(",")
            keys = priority_keyword + main_keyword
            all_pos = _keywords_to_positions(keys, secondary_keywords, cities, keyword)
        return render(request, "keyservice/result.html", {"positions": all_pos, "error": error},)
    else:
        form = SearchForm()
        return render(request, "keyservice/search.html", {"form": form})


def get_map_position(request, *args, **kwargs):
    all_pos, temp, error, seq = [], [], "", 0

    if request.method == "POST":
        form = MapSearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data["site"]
            keywordcitys = KeywordCityRel.objects.filter(keyword_id=keyword.id)

            name = keyword.name
            priority_keyword = keyword.priority_keyword.split(",")
            keys = priority_keyword
            for m_keyword in keys:
                both_key = m_keyword.strip()
                # print(both_key)
                whole_sleep_time = random.randint(147, 360)
                for keywordcity in keywordcitys:
                    print(both_key, keywordcity.city_id.name)
                    sleep_time = random.randint(18, 76)
                    if not _check_map_record(name, both_key, keywordcity.city_id.name):
                        time.sleep(whole_sleep_time)
                        data = _get_map_record(
                            seq, name, both_key, keywordcity.city_id.name, keyword
                        )
                        if isinstance(data, list):
                            for li in data:
                                temp.append(li)
                                li.save()
                        else:
                            temp.append(data)
                            data.save()
                        time.sleep(sleep_time)
                    all_pos = all_pos + temp
                    temp = []
                
        return render(request, "keyservice/result.html", {"positions": all_pos, "error": error},)
    else:
        form = MapSearchForm()
        return render(request, "keyservice/map_search.html", {"form": form})


def get_report(request, *args, **kwargs):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            site = form.cleaned_data["site"]
            date = form.cleaned_data["date"]
            is_map = form.cleaned_data["is_map"]
            if is_map:
                filepath = _get_map_records(site, date)
            else:
                filepath = _get_search_records(site, date)
            return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    else:
        form = ReportForm()
        return render(request, "keyservice/report.html", {"form": form})


def get_graph_report(request, *args, **kwargs):
    if request.method == "POST":
        form = GraphReportForm(request.POST)
        if form.is_valid():
            site = form.cleaned_data["site"]
            interval = form.cleaned_data["interval"]
            today = datetime.today()
            # months to days conversion is months*30 days
            days = int(interval) * 30
            td = timedelta(days=days)
            start_date = today - td
            _get_graph_record(site, start_date.month, start_date.year, today.month, today.year)

            generate_graph(site)
            filepath = os.path.join(PAR_DIR, "graph.zip")
            return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    else:
        form = GraphReportForm()
        return render(request, "keyservice/graph_report.html", {"form": form})


def upload_file(request, *args, **kwargs):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]
            if not csv_file.name.endswith(".csv"):
                return render(request, "keyservice/upload.html", {"status": False})
            handle_uploaded_file(csv_file)
            return render(request, "keyservice/upload.html", {"status": True})
    else:
        form = UploadFileForm()
    return render(request, "keyservice/upload.html", {"form": form})
def upload_file_map(request, *args, **kwargs):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]
            if not csv_file.name.endswith(".csv"):
                return render(request, "keyservice/upload.html", {"status": False})
            map_upload(csv_file)
            return render(request, "keyservice/upload.html", {"status": True})
    else:
        form = UploadFileForm()
    return render(request, "keyservice/upload.html", {"form": form})


def delete_positions(request, *args, **kwargs):
    if request.method == "POST":
        positions = Position.objects.all()
        for position in positions:
            position.delete()
        return render(request, "keyservice/delete.html", {"status": False})
    else:
        return render(request, "keyservice/delete.html", {"status": True})


def get_cities(request, *args, **kwargs):
    cities = []
    site_id = request.GET.get("site_id", None)
    print(site_id)
    key_cities = KeywordCityRel.objects.filter(keyword_id__id=site_id)
    for kc in key_cities:
        cities.append(kc.city_id)
    return render(request, "keyservice/add_cities.html", {"cities": cities})


def get_last_record(request):
    site_id = request.GET.get("site_id", None)
    position = Position.objects.filter(keyword_id__id=site_id).filter(date=date.today()).last()
    return render(request, "keyservice/last_record.html", {"position": position})


def get_urls_from_keyword(request, *args, **kwargs):
    if request.POST:
        form = KeywordToUrlFrom(request.POST)
        # urls = google(request.POST.get("keyword"))
        if form.is_valid():
            url_list = google(request.POST.get("keyword"))
            data = {
                "keyword": form.cleaned_data["keyword"],
                "url_text": " \n".join(url_list),
            }
            data_form = KeywordToUrlFrom(data)
            return render(request, "keyservice/keyword_to_url.html", {"form": data_form})
            # return HttpResponse("ok")
    else:
        form = KeywordToUrlFrom()
        return render(request, "keyservice/keyword_to_url.html", {"form": form})


def test_from(request, *args, **kwargs):
    if request.method == "POST":
        img = request.FILES["image"]
        print(img)
        # form = GraphReportForm(request.POST)
        # if form.is_valid():
        #     site = form.cleaned_data["site"]
        #     interval = form.cleaned_data["interval"]
        #     print(site)
        #     print(type(interval))
        #     return HttpResponse("ok")
        return HttpResponse("failed")
    else:
        form = UploadFileForm()
        return render(request, "keyservice/test.html", {"form": form})

