import os
import json
import csv
import zipfile
import matplotlib.pyplot as plt
from .models import Keyword


def csv_to_dict(file_name):
    """This func read the csv and convert data as dictionary of
     d_dict={'city':{'keyword':[[date], [position]]}},
             'city':{'keyword':[[date], [position]]}},
                    .....                             }"""
    d_dict, k_set, c_set = dict(), set(), set()
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        # Removing header
        header = next(reader)
        # process csv record one by one and convert as dictionary
        # row[0]-->Date, row[1]-->url, row[2]-->keyword, row[3]--city, row[4]-->position
        for row in reader:
            # Check if city is available in dictionary or create city
            key = normalize_data(row[2])
            city = normalize_data(row[3])
            if city in d_dict:
                c_dict = d_dict.get(city)
                # Check if keyword is availble in dictionary or create new keyword
                if key in c_dict:
                    li = c_dict.get(key)
                    date, position = li[0], li[1]
                    date.append(row[0])
                    position.append(row[4])
                else:
                    date, position = list(), list()
                    date.append(row[0])
                    position.append(row[4])
                    c_dict[key] = [date, position]
            else:
                date, position = list(), list()
                date.append(row[0])
                position.append(row[4])
                keyword = {key: [date, position]}
                d_dict[city] = keyword
            # Add cities and keywords in set, it will avoid the duplications
            k_set.add(key)
            c_set.add(city)
        return d_dict, c_set, k_set


def csv_to_dict2(file_name):
    """This func read the csv and convert data as dictionary of
     d_dict={'keyword':{'city':[[date], [position]]}
                         .....
            },
             'keyword':{'city':[[date], [position]]}
                         ......
            },
                    .....                            
    }"""
    d_dict, k_set, c_set = dict(), set(), set()
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        # Removing header
        header = next(reader)
        # process csv record one by one and convert as dictionary
        # row[0]-->Date, row[1]-->url, row[2]-->keyword, row[3]--city, row[4]-->position
        for row in reader:
            # Check if city is available in dictionary or create city
            key = normalize_data(row[2])
            city = normalize_data(row[3])
            if key in d_dict:
                c_dict = d_dict.get(key)
                # Check if keyword is availble in dictionary or create new keyword
                if city in c_dict:
                    li = c_dict.get(city)
                    date, position = li[0], li[1]
                    date.append(row[0])
                    position.append(row[4])
                else:
                    date, position = list(), list()
                    date.append(row[0])
                    position.append(row[4])
                    c_dict[city] = [date, position]
            else:
                date, position = list(), list()
                date.append(row[0])
                position.append(row[4])
                keyword = {city: [date, position]}
                d_dict[key] = keyword
            # Add cities and keywords in set, it will avoid the duplications
            k_set.add(key)
            c_set.add(city)
        # print(k_set)
    # with open("sample.json", "w") as outfile:
    #     json.dump(d_dict, outfile)
    return d_dict, c_set, k_set


def normalize_data(key):
    return key.strip()


def normalize_date(date_list):
    """Change the date as mm-yyyy from yyyy/mm/dd"""
    x_li = list()
    for x in date_list:
        date = x.split("-")
        d = date[1] + "-" + date[0]
        x_li.append(d)
    return x_li


def normalize_position(position_list):
    """Change the position string to integer using int() func"""
    y_li = list()
    for y in position_list:
        y_li.append(int(y))
    return y_li


def generate_report(data_dict, city_set, keyword_set):
    # Generate report city vise
    for city in data_dict:
        index = 1
        report = city + "-line-report.pdf"
        write_path = os.path.join("graph", report)
        plt.figure(figsize=(12, 120))
        graph_keywords = data_dict.get(city)
        for keyword in graph_keywords:
            #        for count in range(len(graph_keywords)):
            #            keyword=get_priority()
            graph = graph_keywords.get(keyword)
            date = graph[0]
            position = graph[1]

            if len(date) > 2 and index < 82:
                x_list = normalize_date(date)
                y_list = normalize_position(position)

                plt.subplot(60, 2, index)
                plt.plot(x_list, y_list, marker="o", label=city)
                plt.ylim(0, 20)
                plt.title(keyword)
                plt.legend()

                index += 1
        plt.tight_layout()
        plt.savefig(write_path, dpi=300)
    return


def generate_report2(data_dict, city_set, keyword_set):
    # Generate report city vise
    for city in data_dict:
        index = 1
        report = city + "-bar-report.pdf"
        write_path = os.path.join("graph", report)
        plt.figure(figsize=(12, 120))
        graph_keywords = data_dict.get(city)
        for keyword in graph_keywords:
            #        for count in range(len(graph_keywords)):
            #            keyword=get_priority()
            graph = graph_keywords.get(keyword)
            date = graph[0]
            position = graph[1]

            if len(date) > 2 and index < 82:
                x_list = normalize_date(date)
                y_list = normalize_position(position)

                plt.subplot(60, 2, index)
                plt.bar(x_list, y_list, label=city)
                plt.ylim(0, 20)
                plt.title(keyword)
                plt.legend()

                index += 1
        plt.tight_layout()
        plt.savefig(write_path, dpi=300)
    return


def get_priority(priority):
    # print(priority)
    if len(priority) != 0:
        prority_list = priority.split(",")
        return prority_list
    else:
        return list()


def generate_report3(data_dict2, city_set, keyword_set, site):
    plt.figure(figsize=(7, 320))
    # Generate report keyword vise
    index = 1
    #    for keyword in data_dict2:

    keyword = site
    title = keyword.title
    priority_str = keyword.priority_keyword
    # print(site, priority_str)
    report = title + "-report.pdf"
    write_path = os.path.join("graph", report)
    priority_keyword_list = get_priority(priority_str)
    for count in range(len(data_dict2)):
        # print("...")
        if priority_keyword_list:
            keyword = priority_keyword_list.pop()
            # print(keyword)
            graph_keywords = data_dict2.get(keyword.strip())
            # print("..", graph_keywords)
            plt.subplot(99, 1, index)
            if graph_keywords is not None:
                for city in graph_keywords:
                    graph = graph_keywords.get(city)

                    date = graph[0]
                    position = graph[1]

                    x_list = normalize_date(date)
                    y_list = normalize_position(position)

                    plt.plot(x_list, y_list, marker="o", label=city)

            plt.ylim(0, 20)
            plt.title(keyword)
            plt.legend()
            index += 1
    plt.tight_layout()
    plt.savefig(write_path, dpi=300)
    return


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def list_file(path):
    for name in os.listdir(path):
        file = os.path.join(path, name)
        if os.path.isfile(file):
            os.remove(file)
    print("file removed")


def generate_graph(site):
    file = "graph_position.csv"
    data_dict, city_set, keyword_set = dict(), set(), set()
    data_dict2, city_set2, keyword_set2 = dict(), set(), set()
    data_dict, city_set, keyword_set = csv_to_dict(file)

    generate_report(data_dict, city_set, keyword_set)
    generate_report2(data_dict, city_set, keyword_set)
    data_dict2, city_set2, keyword_set2 = csv_to_dict2(file)
    generate_report3(data_dict2, city_set2, keyword_set2, site)

    zipf = zipfile.ZipFile("graph.zip", "w", zipfile.ZIP_DEFLATED)
    zipdir("graph/", zipf)
    zipf.close()

    list_file("graph/")

