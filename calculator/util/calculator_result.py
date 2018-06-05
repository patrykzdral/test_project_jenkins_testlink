class CalculatorResult(object):

    def __init__(self, nearest_reference_city=None,
                 distance_from_flat_to_nearest_reference_city=None):
        self._nearest_reference_city = nearest_reference_city
        self._distance_from_flat_to_nearest_reference_city \
            = distance_from_flat_to_nearest_reference_city
        self._final_price_per_meter = None
        self._house_price = None
        self._basic_price_per_meter = None

    @property
    def nearest_reference_city(self):
        return self._nearest_reference_city

    @nearest_reference_city.setter
    def nearest_reference_city(self, nearest_reference_city):
        self._nearest_reference_city = nearest_reference_city

    @property
    def distance_from_flat_to_nearest_reference_city(self):
        return self._distance_from_flat_to_nearest_reference_city

    @distance_from_flat_to_nearest_reference_city.setter
    def distance_from_flat_to_nearest_reference_city(self, distance):
        self._distance_from_flat_to_nearest_reference_city \
            = distance

    @property
    def basic_price_per_meter(self):
        return self._basic_price_per_meter

    @basic_price_per_meter.setter
    def basic_price_per_meter(self, basic_price_per_meter):
        self._basic_price_per_meter = basic_price_per_meter

    @property
    def house_price(self):
        return self._house_price

    @house_price.setter
    def house_price(self, house_price):
        self._house_price = house_price

    @property
    def final_price_per_meter(self):
        return self._final_price_per_meter

    @final_price_per_meter.setter
    def final_price_per_meter(self, final_price_per_meter):
        self._final_price_per_meter = final_price_per_meter

