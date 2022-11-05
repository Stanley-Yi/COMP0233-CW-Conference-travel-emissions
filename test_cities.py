import pytest
from cities import City, CityCollection
from utils import *
from pathlib import Path

# conda activate intern_pytorch
# cd D:\Files\Learning Materials\Postgraduate\Semester 1\COMP0233\Coursework
# pytest test_cities.py

# test data
Algiers = City("Algiers", "Algeria", 1, 28.0000272, 2.9999825)
Buenos_Aires = City("Buenos Aires", "Argentina", 5, -34.6075616, -58.437076)
Mendoza = City("Mendoza", "Argentina", 4, -34.78719615, -68.4380712382687)
Birmingham_Gardens = City("Birmingham Gardens", "Australia", 1, -68.4380712382687, 151.69)
Sidney = City("Sidney", "Canada", 6, 48.6505788, -123.3983246)


# Test City Constructor
def test_valid_values_City_Constructor():
    City("Algeria", "Algiers", 1, 28.0000272, 2.9999825)

def test_invalid_values_City_name():
    with pytest.raises(TypeError, match=r"City name should be string"):
        City([234], "Algiers", 1, 1.0, 2)

def test_invalid_values_City_country():
    with pytest.raises(TypeError, match=r"Country name should be string"):
        City("Algeria", 2.3, 1, 1.0, 2)

def test_invalid_values_City_num():
    with pytest.raises(TypeError, match=r"Attendees number should be an integer"):
        City("Algeria", "Algiers", 1.358, 1.0, 2)

def test_invalid_values_City_latitude():
    with pytest.raises(TypeError, match=r"Latitude and longitude should be decimal numbers"):
        City("Algeria", "Algiers", 1, 'ffsda', 2)

def test_invalid_values_City_longitude():
    with pytest.raises(TypeError, match=r"Latitude and longitude should be decimal numbers"):
        City("Algeria", "Algiers", 1, 1.0, [2.75])

def test_invalid_ranges_City_num():
    with pytest.raises(Exception, match=r"Attendees should be a positive number"):
        City("Algeria", "Algiers", -113, 28.0000272, 2.9999825)

def test_invalid_ranges_City_latitude():
    with pytest.raises(Exception, match=r"Latitude should be in the range of -90 to 90"):
        City("Algeria", "Algiers", 1, -107.26, 2.9999825)

    with pytest.raises(Exception, match=r"Latitude should be in the range of -90 to 90"):
        City("Algeria", "Algiers", 1, 188.57, 2.9999825)

def test_invalid_ranges_City_longitude():
    with pytest.raises(Exception, match=r"Longitude should be in the range of -180 to 180"):
        City("Algeria", "Algiers", 1, 28.0000272, -208)

    with pytest.raises(Exception, match=r"Longitude should be in the range of -180 to 180"):
        City("Algeria", "Algiers", 1, 28.0000272, 365)


# Test CityCollection Constructor
def test_valid_values_CityCollection_Constructor():
    city_list = [Algiers, Buenos_Aires]
    cities = CityCollection(city_list)
    assert cities.cities == city_list

def test_invalid_values_CityCollection_cities():
    with pytest.raises(Exception, match=r"Cities should not be empty or None"):
        city_list = []
        CityCollection(city_list)

    with pytest.raises(Exception, match=r"Cities should not be empty or None"):
        city_list = None
        CityCollection(city_list)

def test_invalid_Types_CityCollection_cities():
    with pytest.raises(TypeError, match=r"Cities should be a list of City object"):
        city_list = {"Algeria": 1}
        CityCollection(city_list)

    with pytest.raises(TypeError, match=r"Cities should be a list of City object"):
        wrong_city = []
        city_list = [Algiers, wrong_city]
        CityCollection(city_list)


# Test read_attendees_file
def test_read_attendees_file():
    file = Path('attendee_locations.csv')
    read_attendees_file(file)


# Test city.distance_to
def test_City_distance_to():
    distance = Algiers.distance_to(Buenos_Aires)
    assert int(distance) == 9492  # https://www.omnicalculator.com/other/latitude-longitude-distance

def test_invaild_distance_to():
    with pytest.raises(Exception, match=r"Function distance_to should take a City object as argument"):
        Algiers.distance_to([Buenos_Aires])


# Test city.co2_to
def test_City_co2_to():
    co2 = Algiers.co2_to(Buenos_Aires)
    assert co2 == Algiers.distance_to(Buenos_Aires) * 300 * Algiers.num

def test_invaild_co2_to():
    with pytest.raises(Exception, match=r"Function co2_to should take a City object as argument"):
        wrong_city = "City"
        Algiers.co2_to(wrong_city)


# Test CityCollection.countries
def test_CityCollection_countries():
    city_collection = CityCollection([Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens])
    assert set(city_collection.countries()) == {'Algeria', 'Australia', 'Argentina'}


# Test CityCollection.total_attendees
def test_CityCollection_total_attendees():
    city_collection = CityCollection([Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens])
    assert city_collection.total_attendees() == 11


# Test CityCollection.total_distance_travel_to
def test_CityCollection_total_distance_travel_to():
    l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens, Sidney]
    city_collection = CityCollection(l)

    # calculate true value
    true_dis = 0.0
    for i in l:
        true_dis += i.distance_to(Sidney) * i.num

    assert city_collection.total_distance_travel_to(Sidney) == true_dis

def test_invaild_total_distance_travel_to():
    with pytest.raises(Exception, match=r"Function total_distance_travel_to should take a City object as argument"):
        l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens]
        city_collection = CityCollection(l)
        wrong_city = "City"
        city_collection.total_distance_travel_to(wrong_city)


# Test CityCollection.travel_by_country
def test_CityCollection_travel_by_country():
    l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens, Sidney]
    city_collection = CityCollection(l)

    # calculate true value
    true_dic = {'Algeria':0.0, 'Argentina':0.0, 'Australia':0.0, 'Canada':0.0}
    for i in l:
        true_dic[i.country] += i.distance_to(Sidney) * i.num

    assert city_collection.travel_by_country(Sidney) == true_dic

def test_invaild_travel_by_country():
    with pytest.raises(Exception, match=r"Function travel_by_country should take a City object as argument"):
        l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens]
        city_collection = CityCollection(l)
        wrong_city = "City"
        city_collection.travel_by_country(wrong_city)


# Test CityCollection.co2_by_country
def test_CityCollection_co2_by_country():
    l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens, Sidney]
    city_collection = CityCollection(l)

    # calculate true value
    true_dic = {'Algeria':0.0, 'Argentina':0.0, 'Australia':0.0, 'Canada':0.0}
    for i in l:
        true_dic[i.country] += i.co2_to(Sidney)

    assert city_collection.co2_by_country(Sidney) == true_dic

def test_invaild_co2_by_country():
    with pytest.raises(Exception, match=r"Function co2_by_country should take a City object as argument"):
        l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens]
        city_collection = CityCollection(l)
        wrong_city = {}
        city_collection.co2_by_country(wrong_city)


# Test CityCollection.total_co2
def test_CityCollection_total_co2():
    l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens, Sidney]
    city_collection = CityCollection(l)

    # calculate true value
    true_value = 0.0
    for i in l:
        true_value += i.co2_to(Sidney)

    assert round(city_collection.total_co2(Sidney), 6) == round(true_value, 6)

def test_invaild_total_co2():
    with pytest.raises(Exception, match=r"Function total_co2 should take a City object as argument"):
        l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens]
        city_collection = CityCollection(l)
        wrong_city = (1, 2)
        city_collection.total_co2(wrong_city)


# Test CityCollection.summary
def test_CityCollection_summary(capsys):
    l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens, Sidney]
    city_collection = CityCollection(l)

    city_collection.summary(Sidney)
    out, err = capsys.readouterr()

    true_output = "Host city: Sidney (Canada)\nTotal CO2: 37216 tonnes\nTotal attendees travelling to Sidney from 4 different cities: 11\n"

    assert out == true_output

def test_invaild_summary():
    with pytest.raises(Exception, match=r"Function summary should take a City object as argument"):
        l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens]
        city_collection = CityCollection(l)
        wrong_city = [1, 2]
        city_collection.summary(wrong_city)


# Test CityCollection.sorted_by_emissions
def test_CityCollection_sorted_by_emissions():
    l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens, Sidney]
    city_collection = CityCollection(l)

    output = city_collection.sorted_by_emissions()

    # calculate true value
    true_result = []
    for i in l:
        true_result.append((i.name, city_collection.total_co2(i)))

    true_result = sorted(true_result, key=lambda x: x[:][1])

    assert output == true_result


# Test CityCollection.plot_top_emitters
def test_CityCollection_plot_top_emitters():
    file = Path('attendee_locations.csv')
    city_collection = read_attendees_file(file)

    city_collection.plot_top_emitters(Birmingham_Gardens, 8, True)

def test_invalid_Types_plot_top_emitters():
    l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens, Sidney]
    city_collection = CityCollection(l)

    with pytest.raises(TypeError, match=r"Argument city should be a City object"):
        wrong_city = [1, 2]
        city_collection.plot_top_emitters(wrong_city, 8, True)

    with pytest.raises(TypeError, match=r"Argument n should be integer"):
        city_collection.plot_top_emitters(Birmingham_Gardens, '10', True)

    with pytest.raises(Exception):
        city_collection.plot_top_emitters(Birmingham_Gardens, 10, True)

    with pytest.raises(TypeError, match=r"Argument save should be boolean"):
        city_collection.plot_top_emitters(Birmingham_Gardens, 3, 'true')




if __name__ == '__main__':
    l = [Algiers, Buenos_Aires, Mendoza, Birmingham_Gardens, Sidney]
    city_collection = CityCollection(l)

    output = city_collection.plot_top_emitters(Birmingham_Gardens, 5, True)
    # a = (1, 2)
    # print(output)