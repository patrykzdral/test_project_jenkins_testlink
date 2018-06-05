class ReferenceCity(object):

    def __init__(self, name: object, price_per_meter_on_primary_market: object,
                 price_per_meter_on_aftermarket: object,
                 latitude: object,
                 longitude: object) -> object:
        self._name = name
        self._price_per_meter_on_primary_market \
            = price_per_meter_on_primary_market
        self._price_per_meter_on_aftermarket = price_per_meter_on_aftermarket
        self._latitude = latitude
        self._longitude = longitude

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def price_per_meter_on_primary_market(self):
        return self._price_per_meter_on_primary_market

    @price_per_meter_on_primary_market.setter
    def price_per_meter_on_primary_market(self,
                                          price_per_meter_on_primary_market):
        self._price_per_meter_on_primary_market \
            = price_per_meter_on_primary_market

    @property
    def price_per_meter_on_aftermarket(self):
        return self._price_per_meter_on_aftermarket

    @price_per_meter_on_aftermarket.setter
    def price_per_meter_on_aftermarket(self, price_per_meter_on_aftermarket):
        self._price_per_meter_on_aftermarket = price_per_meter_on_aftermarket

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        self._latitude = latitude

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        self._longitude = longitude
