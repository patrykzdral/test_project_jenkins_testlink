import calculator.util
from calculator.prices_calculator import PricesCalculator

address = calculator.util.Address("", 49.95153, 18.609122)
calculator = PricesCalculator("AIzaSyBEmx5P3vl4ox4OU6nPgwTbU9k-_0Zm6Lo")
calculator.selected_address = address
calculator_result \
    = calculator.calculate_house_price("blok", "pierwotny", "cegła", 1990, 25, False,
                                       False, False, True, True, False, False)

print(str(calculator_result.house_price))

print(str(calculator_result.nearest_reference_city.name))
