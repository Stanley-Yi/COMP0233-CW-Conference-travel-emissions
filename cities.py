from typing import Dict, List, Tuple
import math
import matplotlib.pyplot as plt

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
        # calculate distance km between two cities
        if not type(other) is City:
            raise TypeError("Function distance_to should take a City object as argument")

        # transfer degree to radian
        lon1, lat1, lon2, lat2 = map(math.radians, [self.longitude, self.latitude, other.longitude, other.latitude])

        return 2.0 * 6371.0 * math.asin(math.sqrt((math.sin((lat2 - lat1) / 2) ** 2) + math.cos(lat1) * math.cos(lat2) * (math.sin((lon2 - lon1) / 2)** 2)))


    def co2_to(self, other: 'City') -> float:
        # calculate co2 emitted by all attendees travel from src city to tar city
        if not type(other) is City:
            raise TypeError("Function co2_to should take a City object as argument")

        distance = self.distance_to(other)

        if distance <= 1000:
            return distance * self.num * 200.0
        elif 1000 < distance <= 8000:
            return distance * self.num * 250.0
        else:  # > 8000
            return distance * self.num * 300.0


class CityCollection:
    def __init__(self, cities: List[City]):
        if cities == None or len(cities) == 0:
            raise Exception("Cities should not be empty or None")

        if not type(cities) is list or not all(list(map(self.checkCity, cities))):
            raise TypeError("Cities should be a list of City object")

        self.cities = cities


    def checkCity(self, l: list):
        # check if all element in a list belongs to City class
        return isinstance(l, City)


    def countries(self) -> List[str]:
        # find number of country
        country = []
        for i in self.cities:
            country.append(i.country)
        return list(set(country))  # find unique country by set


    def total_attendees(self) -> int:
        # calculate total attendees
        total_num = 0
        for i in self.cities:
            total_num += i.num
        return total_num


    def total_distance_travel_to(self, city: City) -> float:
        # calculate total distance travelled by all attendees
        if not type(city) is City:
            raise TypeError("Function total_distance_travel_to should take a City object as argument")

        total_distance = 0.0
        for i in self.cities:
            if i.name != city:
                dis = city.distance_to(i)  # distance to host city
                total_distance += dis * i.num
        return total_distance


    def travel_by_country(self, city: City) -> Dict[str, float]:
        # find the total distance of attendees that from the same country to the host city
        if not type(city) is City:
            raise TypeError("Function travel_by_country should take a City object as argument")

        dic = {}
        for i in self.cities:
            if not i.country in dic:  # put country into dict
                dic[i.country] = 0.0

            if i.name != city:
                dis = city.distance_to(i) * i.num  # distance from src city to tar city
                dic[i.country] += dis
        return dic


    def total_co2(self, city: City) -> float:
        # calculate total co2 emitted by all attendees
        if not type(city) is City:
            raise TypeError("Function total_co2 should take a City object as argument")

        total_co2 = 0.0
        dic = self.co2_by_country(city)  # get co2 emitted by attendees from each country

        for v in dic.values():
            total_co2 += v

        return total_co2


    def co2_by_country(self, city: City) -> Dict[str, float]:
        # find the total co2 emitted by attendees that from the same country to the host city
        if not type(city) is City:
            raise TypeError("Function co2_by_country should take a City object as argument")

        dic = {}
        for i in self.cities:
            if not i.country in dic:  # put country into dict
                dic[i.country] = 0.0

            if i.name != city:
                co2 = i.co2_to(city)  # co2 emitted from src city to tar city
                dic[i.country] += co2
        return dic


    def summary(self, city: City):
        # print Host city, total co2, and other relevant info
        if not type(city) is City:
            raise TypeError("Function summary should take a City object as argument")

        city_list = []
        for i in self.cities:
            if i != city:
                city_list.append(i.name)

        total_co2 = self.total_co2(city)
        total_att = self.total_attendees() - city.num
        total_city = len(set(city_list))

        print("Host city: %s (%s)" %(city.name, city.country))
        print("Total CO2: %d tonnes" %(round(total_co2 / 1000)))
        print("Total attendees travelling to %s from %d different cities: %d" %(city.name, total_city, total_att))


    def sorted_by_emissions(self) -> List[Tuple[str, float]]:
        # sort the list of host city names and its total CO2 emissions
        result = []
        for i in self.cities:
            result.append((i.name, self.total_co2(i)))

        return sorted(result, key=lambda x : x[:][1])  # sort list by co2 emissions


    def plot_top_emitters(self, city: City, n = 10, save = False):
        # plot and save n-1 top top emitters and the sum of the others
        if not type(city) is City:
            raise TypeError("Argument city should be a City object")

        if not type(n) is int:
            raise TypeError("Argument n should be integer")

        country_num = len(self.countries())
        if not 0 <= n <= country_num + 1:
            raise Exception("Range of argument n should be [0, total country + 1], total country is %d" %country_num)

        if not type(save) is bool:
            raise TypeError("Argument save should be boolean")

        dic = self.co2_by_country(city)
        top_list = sorted(dic.items(), key=lambda item: item[1], reverse=True)  # sort descending by co2

        # plot
        y = []
        x = []
        All_other_countries = 0.0
        for i in range(len(top_list)):
            if i < n - 1:
                x.append(top_list[i][0])
                y.append(float(top_list[i][1]) / 1000)  # transfer to tonnes
            else:
                All_other_countries += top_list[i][1]

        y.append(All_other_countries / 1000)
        x.append('All other\ncountries')

        plt.title('Total emissions from each country (top %d)' %(n-1))
        plt.ylabel('Total emissions (tonnes CO2)')
        plt.xticks(rotation=60)
        color = ['#1AE6E6', '#22DD48', '#EE1196', '#FFFF00', '#A93CC4']
        plt.bar(x = x, width = 0.35, height = y, edgecolor = 'white', color = color, tick_label = x)

        if save:  # save img
            img_name = city.name.replace(" ", "_").lower()
            plt.savefig("./%s.png" %img_name, dpi=200, bbox_inches='tight')

        plt.show()

