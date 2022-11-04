from typing import Dict, List, Tuple

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
        raise NotImplementedError

    def co2_to(self, other: 'City') -> float:
        raise NotImplementedError

class CityCollection:
    ...

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

if __name__ == '__main__':
    z = City("fs", "sdafa", 1, 1.0, 2)