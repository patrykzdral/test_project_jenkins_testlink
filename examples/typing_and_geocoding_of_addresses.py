from calculator.prices_calculator import PricesCalculator
calculator = PricesCalculator("AIzaSyBEmx5P3vl4ox4OU6nPgwTbU9k-_0Zm6Lo")
calculator.autocomplete_addresses = "Kolorowa 12"
print(calculator.autocomplete_addresses)
