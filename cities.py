from typing import Dict, List, Tuple
import math

class City:
    def __init__(self, name: str, country: str, num: int, latitude: float, longitude: float):
        if not type(name) is str:
            raise TypeError("City name should be string")

        if not type(country) is str:
            raise TypeError("Country name should be string")

        if not type(num) is int:
            raise TypeError("Attendees number should be an integer")

        if not (type(latitude) is int or type(latitude) is float) or not (type(longitude) is int or type(longitude) is float):
            raise TypeError("Latitude and longitude should be decimal numbers")

        if num < 0:
            raise Exception("Attendees should be a positive number")

        if latitude < -90 or latitude > 90:
            raise Exception("Latitude should be in the range of -90 to 90")

        if longitude < -180 or longitude > 180:
            raise Exception("Longitude should be in the range of -180 to 180")

        self.name = name
        self.country = country
        self.num = num
        self.latitude = latitude
        self.longitude = longitude


    def distance_to(self, other: 'City') -> float:
        if not type(other) is City:
            raise TypeError("Function distance_to should take a City object as argument")

        lon1, lat1, lon2, lat2 = map(math.radians, [self.longitude, self.latitude, other.longitude, other.latitude])

        return 2.0 * 6371.0 * math.asin(math.sqrt((math.sin((lat2 - lat1) / 2) ** 2) + math.cos(lat1) * math.cos(lat2) * (math.sin((lon2 - lon1) / 2)** 2)))


    def co2_to(self, other: 'City') -> float:
        if not type(other) is City:
            raise TypeError("Function co2_to should take a City object as argument")

        distance = self.distance_to(other)

        if distance <= 1000:
            return distance * self.num * 200.0
        elif 1000 < distance <= 8000:
            return distance * self.num * 250.0
        else:
            return distance * self.num * 300.0


class CityCollection:
    def __init__(self, cities: List[City]):
        if cities == None or len(cities) == 0:
            raise Exception("Cities should not be empty or None")

        if not type(cities) is list or not all(list(map(self.checkCity, cities))):
            raise TypeError("Cities should be a list of City object")

        self.cities = cities


    def checkCity(self, l: list):
        return isinstance(l, City)


    def countries(self) -> List[str]:
        raise NotImplementedError

    def total_attendees(self) -> int:
        raise NotImplementedError

    def total_distance_travel_to(self, city: City) -> float:
        raise NotImplementedError

    def travel_by_country(self, city: City) -> Dict[str, float]:
        raise NotImplementedError

    def total_co2(self, city: City) -> float:
        raise NotImplementedError

    def co2_by_country(self, city: City) -> Dict[str, float]:
        raise NotImplementedError

    def summary(self, city: City):
        raise NotImplementedError

    def sorted_by_emissions(self) -> List[Tuple[str, float]]:
        raise NotImplementedError

    def plot_top_emitters(self, city: City, n: int, save: bool):
        raise NotImplementedError