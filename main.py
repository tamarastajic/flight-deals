from flight_search import FlightSearch
from data_manager import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Using Google Sheet API to Get Data ~~~~~~~~~~~~~~~~~~~~~~~~~~
GS_Info = GoogleSheetInfo()
data_manager = DataManager()

sheet_data = data_manager.get_data("prices")
user_data = data_manager.get_data("users")

print(sheet_data)
print(user_data)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Fill Out iataCode ~~~~~~~~~~~~~~~~~~~~~~~~~~
ORIGINAL_CITY = "Belgrade"
flight_search = FlightSearch(ORIGINAL_CITY.title())

change = False
for item in sheet_data:
    if item["IATA Code"] == "":
        change = True
        city = item["City"]
        item["IATA Code"] = flight_search.get_IATA_code(city)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Using Google Sheet API to Update IATA codes if Needed ~~~~~~~~~~~~~~~~~~~~~~~~~~
if change == True:
    list_of_values = [item["IATA Code"] for item in sheet_data]
    range = f"prices!B2:B{len(sheet_data)+1}"
    data_manager.put_data(list_of_values, range, "COLUMNS")

    print(f"Updated columns: {range}")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Acquire New User ~~~~~~~~~~~~~~~~~~~~~~~~~~
# from user_manager import UserManager
# user_manager = UserManager()
# new_user = user_manager.acquire_user()
# user_ord = (len(user_data)) + 2
# range = f"users!A{user_ord}:C{user_ord}"
# data_manager.put_data(new_user, range, "ROWS")
# user_data = data_manager.get_data("users")

# print(f"Updated columns: {range}")
# print(user_data)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Find Flights for All Cities and Sends an SMS if Needed ~~~~~~~~~~~~~~~~~~~~~~~~~~
from notification_manager import NotificationManager
notification_manager = NotificationManager()

flights = []
for item in sheet_data:
    code = item["IATA Code"]
    flight = flight_search.search_flights(item["City"], code)
    if flight.price == "Flights Not Found":
        flights.append(flight)
        continue

    # ---> Sends an SMS if the Price is Lower than the Lowest Price <---
    # if flight.price <= item["Lowest Price"]:
    #     notification_manager.send_message(flight, item["City"])

    # ---> Sends an Email if the Price is Lower than the Lowest Price <---
    if flight.price <= item["Lowest Price"]:
        notification_manager.send_email(flight,user_data)

    flights.append(flight)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Fill out Current Price ~~~~~~~~~~~~~~~~~~~~~~~~~~
flight_prices = [flight.price for flight in flights]
range = f"prices!D2:D{len(flights)+1}"
for flight in flights:
    data_manager.put_data(flight_prices, range, "COLUMNS")

print(f"Updated columns: {range}")
