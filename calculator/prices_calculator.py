import sys
import math
from datetime import datetime

import googlemaps

from calculator import exception
from calculator.util.address import Address
from calculator.util.calculator_result import \
    CalculatorResult
from calculator.util.reference_city import \
    ReferenceCity


class PricesCalculator(object):

    def __init__(self, input_google_api_key):
        self._autocomplete_addresses = []
        self._selected_address = Address

        self._calculator_result = CalculatorResult()

        self._reference_cities = [
            ReferenceCity(name="Gdańsk",
                          price_per_meter_on_primary_market=6596.0,
                          price_per_meter_on_aftermarket=8082.0,
                          latitude=54.372158, longitude=18.638306),

            ReferenceCity(name="Katowice",
                          price_per_meter_on_primary_market=5421.0,
                          price_per_meter_on_aftermarket=4664.0,
                          latitude=50.270908, longitude=19.039993),

            ReferenceCity(name="Kraków",
                          price_per_meter_on_primary_market=7401.0,
                          price_per_meter_on_aftermarket=8013.0,
                          latitude=50.049683, longitude=19.944544),

            ReferenceCity(name="Lublin",
                          price_per_meter_on_primary_market=5378.0,
                          price_per_meter_on_aftermarket=5254.0,
                          latitude=51.246452, longitude=22.568445),

            ReferenceCity(name="Łódź",
                          price_per_meter_on_primary_market=4814.0,
                          price_per_meter_on_aftermarket=4290.0,
                          latitude=51.759445, longitude=19.457216),

            ReferenceCity(name="Poznań",
                          price_per_meter_on_primary_market=6437.0,
                          price_per_meter_on_aftermarket=6344.0,
                          latitude=52.409538, longitude=16.931992),

            ReferenceCity(name="Szczecin",
                          price_per_meter_on_primary_market=5102.0,
                          price_per_meter_on_aftermarket=4691.0,
                          latitude=53.428543, longitude=14.552812),

            ReferenceCity(name="Warszawa",
                          price_per_meter_on_primary_market=8080.0,
                          price_per_meter_on_aftermarket=9457.0,
                          latitude=52.237049, longitude=21.017532),

            ReferenceCity(name="Wrocław",
                          price_per_meter_on_primary_market=6297.0,
                          price_per_meter_on_aftermarket=6495.0,
                          latitude=51.107883, longitude=17.038538),
        ]

        self._market_types = ["pierwotny", "wtórny"]

        self._building_types = {'blok': 1.0, 'kamienica': 0.85,
                                'dom wolnostojący': 1.05,
                                'apartementowiec': 1.15}

        self._building_materials = {'wielka płyta': 0.9, 'pustak': 0.95,
                                    'cegła': 1.0, 'drewno': 0.6,
                                    'żelbeton': 1.15}

        self._additional_attributes = {'balkon': 20000.0, 'piwnica': 10000.0,
                                       'ogródek': 50000.0, 'taras': 40000.0,
                                       'winda': 30000.0,
                                       'oddzielna kuchnia': 30000.0,
                                       'strzeżone osiedle': 50000.0}

        self._google_maps = googlemaps.Client(key=input_google_api_key)

    @property
    def google_maps(self):
        return self._google_maps

    @google_maps.setter
    def google_maps(self, google_maps):
        self._google_maps = google_maps

    @property
    def reference_cities(self):
        return self._reference_cities

    @reference_cities.setter
    def reference_cities(self, reference_cities):
        self._reference_cities = reference_cities

    @property
    def market_types(self):
        return self._market_types

    @market_types.setter
    def market_types(self, market_types):
        self._market_types = market_types

    @property
    def building_types(self):
        return self._building_types

    @building_types.setter
    def building_types(self, building_types):
        self._building_types = building_types

    @property
    def building_materials(self):
        return self._building_materials

    @building_materials.setter
    def building_materials(self, building_materials):
        self._building_materials = building_materials

    @property
    def additional_attributes(self):
        return self._additional_attributes

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes):
        self._additional_attributes = additional_attributes

    @property
    def autocomplete_addresses(self):
        return self._autocomplete_addresses

    @autocomplete_addresses.setter
    def autocomplete_addresses(self, autocomplete_addresses):
        if autocomplete_addresses:
            google_result = self._google_maps.geocode(autocomplete_addresses,
                                                      language="pl")

            if google_result:
                if self._autocomplete_addresses:
                    self._autocomplete_addresses = []

                for address in google_result:
                    for address_component in address['address_components']:
                        if address_component['types'][0] == "country":
                            if address_component['long_name'] == "Polska":
                                self._autocomplete_addresses.append(
                                    Address(address['formatted_address'],
                                            address['geometry']["location"]
                                            ["lat"],
                                            address['geometry']["location"]
                                            ["lng"]))
                                break

    @property
    def selected_address(self):
        return self._selected_address

    @selected_address.setter
    def selected_address(self, selected_address):
        if isinstance(selected_address, int):
            self._selected_address \
                = self._autocomplete_addresses[selected_address]
        else:
            self._selected_address = selected_address

    @property
    def calculator_result(self):
        return self._calculator_result

    @calculator_result.setter
    def calculator_result(self, calculator_result):
        self._calculator_result = calculator_result

    def calculate_house_price(self, building_type, market_type,
                              building_material, construction_year,
                              number_of_meters, is_balcony, is_cellar,
                              is_garden, is_terrace, is_elevator,
                              is_separate_kitchen, is_guarded_estate):
        if building_type not in self._building_types:
            raise exception \
                .FlatParameterMismatchException("wskazany rodzaj zabudowy '"
                                                + building_type
                                                + "' nie istnieje", "")

        if market_type not in self._market_types:
            raise exception \
                .FlatParameterMismatchException("wskazany rodzaj rynku '"
                                                + market_type
                                                + "' nie istnieje", "")

        if building_material not in self._building_materials:
            raise exception \
                .FlatParameterMismatchException("wskazany materiał budynku '"
                                                + building_material
                                                + "' nie istnieje", "")

        meter_price_multiplier = 1.0
        meter_price_multiplier *= \
            self.calculate_multiplier_for_distance_to_nearest_reference_city(
                self.calculate_the_nearest_reference_city())

        if market_type == "pierwotny":
            house_price = self._calculator_result.nearest_reference_city \
                .price_per_meter_on_primary_market
        else:
            house_price = self._calculator_result.nearest_reference_city \
                .price_per_meter_on_aftermarket

        self._calculator_result.basic_price_per_meter \
            = meter_price_multiplier * house_price

        meter_price_multiplier \
            *= self \
            .calculate_multiplier_for_construction_year(construction_year)
        meter_price_multiplier \
            *= self._building_types.get(building_type)
        meter_price_multiplier \
            *= self._building_materials.get(building_material)

        house_price *= meter_price_multiplier
        house_price *= float(number_of_meters)

        if is_balcony:
            house_price += self._additional_attributes.get("balkon")

        if is_cellar:
            house_price += self._additional_attributes.get("piwnica")

        if is_garden:
            house_price += self._additional_attributes.get("ogródek")

        if is_terrace:
            house_price += self._additional_attributes.get("taras")

        if is_elevator:
            house_price += self._additional_attributes.get("winda")

        if is_separate_kitchen:
            house_price += self._additional_attributes.get("oddzielna kuchnia")

        if is_guarded_estate:
            house_price += self._additional_attributes.get("strzeżone osiedle")

        self._calculator_result.house_price = house_price
        self._calculator_result.final_price_per_meter \
            = house_price / float(number_of_meters)

        return self._calculator_result

    @staticmethod
    def calculate_multiplier_for_construction_year(construction_year):
        construction_year = int(construction_year)
        datetime_now_year = datetime.today().year

        if construction_year > datetime_now_year:
            raise exception.ConstructionYearViolationException("rok budowy nie "
                                                               "może być większy "
                                                               "niż obecny", "")

        if construction_year < 1900:
            raise exception.ConstructionYearViolationException("rok budowy nie "
                                                               "może być mniejszy "
                                                               "niż 1900", "")

        if construction_year == datetime_now_year:
            return 1.20
        elif construction_year < (datetime_now_year - 40):
            return 0.80
        else:
            return 1.20 - ((datetime_now_year - construction_year) / 100.0)

    @staticmethod
    def calculate_multiplier_for_distance_to_nearest_reference_city(distance):
        if distance < 1000:
            return 1.1
        elif distance < 4000:
            return 1.0
        elif distance < 10000:
            return 0.95
        elif distance < 20000:
            return 0.90
        elif distance < 35000:
            return 0.85
        elif distance < 47000:
            return 0.80
        elif distance < 60000:
            return 0.77
        elif distance < 75000:
            return 0.74
        elif distance < 90000:
            return 0.72
        else:
            return 0.65

    def calculate_the_nearest_reference_city(self):
        global reference_city
        distances_from_flat_to_reference_cities = dict()
        earth_radius = 6371

        for city in self._reference_cities:
            latitude_distance \
                = math.radians(city.latitude - self._selected_address.latitude)
            longitude_distance \
                = math.radians(city.longitude - self._selected_address
                               .longitude)

            a = math.sin(latitude_distance / 2) \
                * math.sin(latitude_distance / 2) \
                + math.cos(math.radians(self._selected_address.latitude)) \
                * math.cos(math.radians(city.latitude)) \
                * math.sin(longitude_distance / 2) \
                * math.sin(longitude_distance / 2)

            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance_in_meters = earth_radius * c * 1000

            distances_from_flat_to_reference_cities[city] = distance_in_meters

        min_distance = sys.maxsize
        for key, value in distances_from_flat_to_reference_cities.items():
            if min_distance > value:
                min_distance = value
                reference_city = key

        self._calculator_result = CalculatorResult(reference_city,
                                                   min_distance)

        return min_distance


if __name__ == "__main__":
    def str_to_bool(v):
        if v.lower() in ("yes", "true", "t", "y", "1"):
            return "true"
        elif v.lower() in ("no", "false", "f", "n", "0"):
            return ""
        else:
            return "error"


    display_addresses = str(sys.argv[1])
    switch_option = str_to_bool(display_addresses)

    if switch_option == "":
        if sys.argv.__len__() != 17:
            print("Podano niewystarczającą ilość argumentów do "
                  "przeprowadzenia kalkulacji.")
            sys.exit(1)
        else:
            google_api_key = str(sys.argv[2])

            try:
                calc = PricesCalculator(google_api_key)
                geocoded_address = Address("",
                                           float(sys.argv[3]),
                                           float(sys.argv[4]))
                calc.selected_address = geocoded_address
                calc.calculate_house_price(str(sys.argv[5]), str(sys.argv[6]),
                                           str(sys.argv[7]), int(sys.argv[8]),
                                           int(sys.argv[9]),
                                           bool(str_to_bool(sys.argv[10])),
                                           bool(str_to_bool(sys.argv[11])),
                                           bool(str_to_bool(sys.argv[12])),
                                           bool(str_to_bool(sys.argv[13])),
                                           bool(str_to_bool(sys.argv[14])),
                                           bool(str_to_bool(sys.argv[15])),
                                           bool(str_to_bool(sys.argv[16])))

                print("WYNIKI KALKULACJI:")
                print("\t*miasto odniesiania*")
                print("\t\t- nazwa: "
                      + calc.calculator_result.nearest_reference_city.name
                      + ",")

                if str(sys.argv[7]) == "pierwotny":
                    print("\t\t- cena za mkw: "
                          + str(round(calc.calculator_result
                                      .nearest_reference_city
                                      .price_per_meter_on_primary_market, 2))
                          + " zł,")
                else:
                    print("\t\t- cena za mkw: "
                          + str(round(calc.calculator_result
                                      .nearest_reference_city
                                      .price_per_meter_on_aftermarket, 2))
                          + " zł,")

                print("\t\t- odległość: "
                      + str(round(calc.calculator_result
                                  .distance_from_flat_to_nearest_reference_city /
                                  1000, 2)) + " km.")

                print("\t*cena mieszkania*")
                print("\t\t- podstawowa cena za mkw: "
                      + str(round(calc.calculator_result
                                  .basic_price_per_meter, 2)) + " zł,")

                print("\t\t- ostateczna cena za mkw: "
                      + str(round(calc.calculator_result
                                  .final_price_per_meter, 2)) + " zł,")

                print("\t\t- cena: "
                      + str(round(calc.calculator_result
                                  .house_price, 2)) + " zł.")
            except (ValueError, exception.FlatParameterMismatchException,
                    exception.ConstructionYearViolationException) as e:
                print("Błąd kalkulacji: " + str(e) + ".")
                exit(4)

    elif switch_option == "true":
        if sys.argv.__len__() != 4:
            print("Podano niewystarczającą ilość argumentów do "
                  "przeprowadzenia typowania adresów.")
            sys.exit(2)
        else:
            google_api_key = str(sys.argv[2])
            address = str(sys.argv[3])
            calc = PricesCalculator(google_api_key)
            calc.autocomplete_addresses = address
            print("Wynik typowania adresów Google Maps:")
            for google_address in calc.autocomplete_addresses:
                print(google_address.formatted_address + ", lat: "
                      + str(google_address.latitude) + ", lng: "
                      + str(google_address.longitude))
    else:
        print("Niepoprawna wartość co najmniej jednego parametru logicznego.\n"
              "Dopuszczane wartości: yes, true, t, y, 1, no, false, f, n, 0.")
        exit(3)
