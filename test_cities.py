import pytest
from cities import City, CityCollection
from utils import *
from pathlib import Path

# conda activate intern_pytorch
# cd D:\Files\Learning Materials\Postgraduate\Semester 1\COMP0233\Coursework
# pytest test_cities.py

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
    Algeria = City("Algeria", "Algiers", 1, 28.0000272, 2.9999825)
    Argentina = City("Argentina", "Buenos Aires", 5, -34.6075616, -58.437076)
    city_list = [Algeria, Argentina]
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
        Algeria = City("Algeria", "Algiers", 1, 28.0000272, 2.9999825)
        Argentina = []
        city_list = [Algeria, Argentina]
        CityCollection(city_list)


# Test read_attendees_file
def test_read_attendees_file():
    file = Path('attendee_locations.csv')
    read_attendees_file(file)


# Test city.distance_to
def test_City_distance_to():
    Algeria = City("Algeria", "Algiers", 1, 0.0, 0.0)
    Argentina = City("Argentina", "Buenos Aires", 5, 10.0, 10.0)
    distance = Algeria.distance_to(Argentina)
    assert round(distance, 1) == 1568.5  # https://www.omnicalculator.com/other/latitude-longitude-distance

def test_invaild_distance_to():
    with pytest.raises(Exception, match=r"Function distance_to should take a City object as argument"):
        Algeria = City("Algeria", "Algiers", 1, 0.0, 0.0)
        Argentina = [City("Argentina", "Buenos Aires", 5, 10.0, 10.0)]
        Algeria.distance_to(Argentina)


# Test city.co2_to
def test_City_co2_to():
    Algeria = City("Algeria", "Algiers", 1, 0.0, 0.0)
    Argentina = City("Argentina", "Buenos Aires", 5, 10.0, 10.0)
    co2 = Algeria.co2_to(Argentina)
    assert co2 == Algeria.distance_to(Argentina) * 250 * 1

def test_invaild_co2_to():
    with pytest.raises(Exception, match=r"Function co2_to should take a City object as argument"):
        Algeria = City("Algeria", "Algiers", 1, 0.0, 0.0)
        Argentina = "City"
        Algeria.co2_to(Argentina)



if __name__ == '__main__':
    Algeria = City("Algeria", "Algiers", 1, 0.0, 0.0)
    Argentina = City("Argentina", "Buenos Aires", 5, 10.0, 10.0)
    co2 = Algeria.co2_to(Argentina)
    print(co2)
    print(Algeria.distance_to(Argentina) * 250 * 1)
    # round(co2, 1) == Algeria.distance_to(Argentina) * 250 * 1