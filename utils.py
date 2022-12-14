from cities import City, CityCollection
from pathlib import Path
import csv


def read_attendees_file(filepath: Path) -> CityCollection:
    city_list = []
    with open(filepath, encoding='utf-8') as f:  # read csv file
        for row in csv.reader(f):
            city_list.append(row)  # record rows of csv

    city_list = city_list[1:]  # remove header
    for i in range(len(city_list)):
        l = city_list[i]
        city_list[i] = City(l[3], l[1], int(l[0]), float(l[4]), float(l[5]))

    return CityCollection(city_list)  # return CityCollection object