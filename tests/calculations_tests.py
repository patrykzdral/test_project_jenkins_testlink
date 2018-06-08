import time
import unittest
from datetime import datetime

from calculator import exception
from calculator.prices_calculator import PricesCalculator
from calculator import Address


class TestLibrary(unittest.TestCase):

    @property
    def formatted_method_name(self):
        return self._formatted_method_name

    @property
    def exec_time(self):
        return self._exec_time

    @property
    def time_start(self):
        return self._time_start

    @property
    def time_end(self):
        return self._time_end

    def setUp(self):
        self._time_start = time.time()

    def tearDown(self):
        self._time_end = time.time()
        self._exec_time = self._time_end - self._time_start

    def test_too_small_value_of_year(self):
        self._formatted_method_name = "Test testing throwing the Construction" \
                                      " Year Violation Exception if the value" \
                                      " of the construction year is too low" \
                                      " (less than 1900)"
        calc = PricesCalculator("AIzaSyBEmx5P3vl4ox4OU6nPgwTbU9k-_0Zm6Lo")
        address = Address("", 49.95153, 18.609122)
        calc.selected_address = address

        with self.assertRaises(
                exception.ConstructionYearViolationException) as context:
            calc.calculate_house_price("blok", "pierwotny", "drewno",
                                       1500, 25, False, False, False,
                                       True, True, False, False)

        self.assertTrue(
            'rok budowy nie moze byc mniejszy niż 1900' in str(context.exception))

    def test_too_big_value_of_year(self):
        self._formatted_method_name = "Test testing throwing the Construction" \
                                      " Year Violation Exception if the value" \
                                      " of the construction year is too high" \
                                      " (more than present)"
        calc = PricesCalculator("AIzaSyBEmx5P3vl4ox4OU6nPgwTbU9k-_0Zm6Lo")
        address = Address("", 49.95153, 18.609122)
        calc.selected_address = address

        datetime_now_year = datetime.today().year
        with self.assertRaises(
                exception.ConstructionYearViolationException) as context:
            calc.calculate_house_price("blok", "pierwotny", "cegła",
                                       datetime_now_year + 1, 25, False, False,
                                       False,
                                       True, True, False, False)

        self.assertTrue(
            'rok budowy nie moze byc wiekszy niż obecny' in str(context.exception))

    def test_mismatch_building_type(self):
        self._formatted_method_name = "Test testing throwing the Flat" \
                                      " Parameter Mismatch Exception if the value" \
                                      " of the building type is incorrect"
        calc = PricesCalculator("AIzaSyBEmx5P3vl4ox4OU6nPgwTbU9k-_0Zm6Lo")
        address = Address("", 49.95153, 18.609122)
        calc.selected_address = address

        building_type = "bloks"
        with self.assertRaises(
                exception.FlatParameterMismatchException) as context:
            calc.calculate_house_price(building_type, "pierwotny", "drewno",
                                       2000, 25, False, False, False,
                                       True, True, False, False)

        self.assertTrue(
            "wskazany rodzaj zabudowy '" + building_type + "' nie istnieje"
            in str(context.exception))

    def test_mismatch_market_type(self):
        self._formatted_method_name = "Test testing throwing the Flat" \
                                      " Parameter Mismatch Exception if the value" \
                                      " of the market type is incorrect"
        calc = PricesCalculator("AIzaSyBEmx5P3vl4ox4OU6nPgwTbU9k-_0Zm6Lo")
        address = Address("", 49.95153, 18.609122)
        calc.selected_address = address

        market_type = "pierwotFny"
        with self.assertRaises(
                exception.FlatParameterMismatchException) as context:
            calc.calculate_house_price("blok", market_type, "drewno",
                                       2000, 25, False, False, False,
                                       True, True, False, False)

        self.assertTrue(
            "wskazany rodzaj rynku '" + market_type + "' nie istnieje"
            in str(context.exception))

    def test_name_of_reference_city(self):
        self._formatted_method_name = "Test testing calculating a reference city" \
                                      " called Katowice in the case of providing" \
                                      " coordinates of an apartment located in the" \
                                      " city of Czestochowa"
        calc = PricesCalculator("AIzaSyBEmx5P3vl4ox4OU6nPgwTbU9k-_0Zm6Lo")
        address = Address("", 50.8118195, 19.1203094)  # Częstochowa
        calc.selected_address = address

        calculator_result = calc.calculate_house_price("blok", "pierwotny", "drewno",
                                                       2000, 25, False, False, False,
                                                       True, True, False, False)

        self.assertEqual(calculator_result.nearest_reference_city.name, "Katowice")


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
