import requests
from data_manager import TequilaInfo
from flight_data import FlightData

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Class Responsible for Tequilla API Searches ~~~~~~~~~~~~~~~~~~~~~~~~~~
class FlightSearch:

    def __init__(self, original_city):
        self.info = TequilaInfo()
        CITY = original_city
        self.DEPARTURE_LOCATION = self.get_IATA_code(CITY)
        self.DEPARTURE_CITY = CITY

    def get_IATA_code(self, city):
        """A method that gets the IATA Code for inputted city."""
        tequila_params = {
            "term": city,
            "location_types": "city",
            "limit": 1,
        }

        response = requests.get(f"{self.info.TEQUILA_ENDPOINT}/locations/query",
                                headers=self.info.tequila_header, params=tequila_params)
        response.raise_for_status()

        code = response.json()["locations"][0]["code"]

        return code

    def search_flights(self, city, city_iata):
        """A function that searches flights for inputted city."""
        import datetime as dt
        now = dt.datetime.now()

        tomorrow = now + dt.timedelta(days=1)
        date_tomorrow = tomorrow.strftime("%d/%m/%Y")

        after_six_months = tomorrow + dt.timedelta(days=90)
        date_after_six = after_six_months.strftime("%d/%m/%Y")


        tequila_params = {
            "fly_from": self.DEPARTURE_LOCATION,
            "fly_to": city_iata,
            "date_from": date_tomorrow,
            "date_to": date_after_six,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 14,
            "flight_type": "round",
            "one_for_city": 1,
            "stopover_from": 0,
            "stopover_to": 0,
            "max_stopovers": 0,
            "max_sector_stopovers": 0,
            "curr": "USD"
        }

        response = requests.get(f"{self.info.TEQUILA_ENDPOINT}/v2/search",
                                headers=self.info.tequila_header, params=tequila_params)

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {city}. ")
            flight = FlightData(f_iata=self.DEPARTURE_LOCATION, t_IATA=city_iata,
                                cityTo=city, cityFrom="", price="Flights Not Found",
                                airline="", departureTime="", arrivalTime="",
                                r_arrivalTime="",r_departureTime="",
                                nightsInDestination="", availability="",
                                flight_link = "")
            return flight

        data = response.json()["data"]

        # Formatting data
        cityTo = data[0]["cityTo"]
        flyTo = data[0]["flyTo"]
        price = data[0]["price"]
        airline = data[0]["airlines"][0]

        departure = data[0]["route"][0]["local_departure"]
        departure = departure[:16]
        departure = dt.datetime.strptime(departure, "%Y-%m-%dT%H:%M")

        arrival = data[0]["route"][0]["local_arrival"]
        arrival = arrival[:16]
        arrival = dt.datetime.strptime(arrival, "%Y-%m-%dT%H:%M")

        r_departure = data[0]["route"][1]["local_departure"]
        r_departure = r_departure[:16]
        r_departure = dt.datetime.strptime(r_departure, "%Y-%m-%dT%H:%M")

        r_arrival = data[0] ["route"][1]["local_arrival"]
        r_arrival = r_arrival[:16]
        r_arrival = dt.datetime.strptime(r_arrival, "%Y-%m-%dT%H:%M")

        nights = data[0]["nightsInDest"]
        availability = data[0]["availability"]["seats"]

        link = data[0]["deep_link"]

        # Making FlightData Object
        flight = FlightData(f_iata=self.DEPARTURE_LOCATION,
                            t_IATA=flyTo,
                            cityFrom=self.DEPARTURE_CITY,
                            cityTo= cityTo,
                            price=price,
                            airline=airline,
                            departureTime=departure,
                            arrivalTime=arrival,
                            r_departureTime=r_departure,
                            r_arrivalTime=r_arrival,
                            nightsInDestination=nights,
                            availability=availability,
                            flight_link=link)
        return flight

