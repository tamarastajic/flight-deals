# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Class Responsible for Flight Info ~~~~~~~~~~~~~~~~~~~~~~~~~~
class FlightData:
    def __init__(self, f_iata, t_IATA, cityFrom, cityTo, price, airline, departureTime, arrivalTime, r_departureTime, r_arrivalTime, nightsInDestination, availability, flight_link):
        self.from_IATA = f_iata
        self.to_IATA = t_IATA
        self.fromCity = cityFrom
        self.toCity = cityTo
        self.price = price
        self.airline = airline
        self.departure = departureTime
        self.arrival = arrivalTime
        self.r_departure = r_departureTime
        self.r_arrival = r_arrivalTime
        self.nights = nightsInDestination
        self.availability = availability
        self.link = flight_link
