class Address(object):

    def __init__(self, formatted_address=None, latitude=None, longitude=None):
        self._longitude = longitude
        self._latitude = latitude
        self._formatted_address = formatted_address

    @property
    def formatted_address(self):
        return self._formatted_address

    @formatted_address.setter
    def formatted_address(self, formatted_address):
        self._formatted_address = formatted_address

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

    def __str__(self):
        return self._formatted_address

    def __repr__(self):
        return self._formatted_address
