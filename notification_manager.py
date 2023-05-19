from data_manager import TwilioInfo
from data_manager import EmailInfo
from data_manager import DataManager
from twilio.rest import Client


# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Class Responsible for Sending Messages and Emails ~~~~~~~~~~~~~~~~~~~~~~~~~~
class NotificationManager:
    def __init__(self):
        self.TwilioInfo = TwilioInfo()
        self.EmailInfo = EmailInfo()

    def send_message(self, flight, city):
        """A method that sends an SMS about the current flight deal."""
        text = f"Guess what? The flight to {city} is currently only ${flight.price}. Departure: {flight.departure}. " \
               f"Arrival: {flight.arrival}"
        client = Client(self.TwilioInfo.TWILIO_SID, self.TwilioInfo.TWILIO_TOKEN)
        message = client.messages \
            .create(
            body=text,
            from_= self.TwilioInfo.FROM_NUMBER,
            to= self.TwilioInfo.TO_NUMBER
                   )
        print(message.status)

    def send_email(self, flight, user_data):
        """A method that sends an email about the current flight deal."""
        import smtplib

        data_manager = DataManager()
        link = data_manager.shorten_link(flight.link)

        for user in user_data:
            to_email = user["Email"]
            to_name = user["First Name"]
            if flight.availability == 1:
                message = f"Hello, {to_name}👋.\nDo you want to go from {flight.fromCity} to {flight.toCity} for ${flight.price}?\n\n" \
                          f"✈  Flight Specifics:  ✈\n" \
                          f"• Airline: {flight.airline}\n" \
                          f"• Number of Nights: {flight.nights}\n\n" \
                          f"• Flight to {flight.toCity}:\n" \
                          f"➡ Exact Departure: {flight.departure}\n" \
                          f"⬅ Exact Arrival: {flight.arrival}\n\n" \
                          f"• Return Flight from {flight.toCity}:\n"\
                          f"➡Departure: {flight.r_departure}\n" \
                          f"⬅Arrival: {flight.r_arrival}\n\n" \
                          f"• Link:{link}.\n\n" \
                          f"⌚ But, hurry... there is only 1 seat available."
            else:
                message = f"Hello, {to_name}👋.\nDo you want to go from {flight.fromCity} to {flight.toCity} for ${flight.price}?\n\n" \
                          f"✈  Flight Specifics:  ✈\n" \
                          f"• Airline: {flight.airline}\n" \
                          f"• Number of Nights: {flight.nights}\n\n" \
                          f"• Flight to {flight.toCity}:\n" \
                          f"➡ Exact Departure: {flight.departure}\n" \
                          f"⬅ Exact Arrival: {flight.arrival}\n\n" \
                          f"• Return Flight from {flight.toCity}:\n" \
                          f"➡Departure: {flight.r_departure}\n" \
                          f"⬅Arrival: {flight.r_arrival}\n\n" \
                          f"• Link:{link}.\n\n" \
                          f"⌚ But, hurry... there are only {flight.availability} seats available."

            connection = smtplib.SMTP("smtp.gmail.com", port=587)
            connection.starttls()
            connection.login(user=self.EmailInfo.EMAIL, password=self.EmailInfo.PASSWORD)
            connection.sendmail(
                from_addr=self.EmailInfo.EMAIL,
                to_addrs=to_email,
                msg=f"Subject: ✈ Cheap Flight to {flight.toCity} FOUND ✈\n\n{message}".encode('utf-8')
            )
            print(f"Email for {flight.toCity} sent to: {user['First Name']} {user['Last Name']}")




