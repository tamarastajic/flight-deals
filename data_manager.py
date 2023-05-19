import requests

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Classes for Each Needed API Data ~~~~~~~~~~~~~~~~~~~~~~~~~~

# Input your own data!
class GoogleSheetInfo:
    def __init__(self):
        self.GOOGLE_SHEET_ID = YOUR GOOGLE SHEET ID
        self.GOOGLE_SHEET_ACCESS_TOKEN = YOUR GOOGLE SHEET ACCESS TOKEN
        self.GOOGLE_SHEETS_ENDPOINT = f"https://sheets.googleapis.com/v4/spreadsheets"
        self.GOOGLE_SHEETS_HEADING = {'authorization': f'Bearer {self.GOOGLE_SHEET_ACCESS_TOKEN}',
                                 'Content-Type': 'application/vnd.api+json'}

class CuttlyINFO:
    def __init__(self):
        self.CUTTLY_ENDPOINT = "http://cutt.ly/api/api.php"
        self.CUTTLY_KEY = YOUR CUTTLY KEY

class TequilaInfo:
    def __init__(self):
        self.TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
        self.TEQUILA_API_KEY = YOUR TEQUILA API KEY

        self.tequila_header = {
            "apikey": self.TEQUILA_API_KEY
        }

class TwilioInfo:
    def __init__(self):
        self.TWILIO_SID = YOUR TWILIO SID
        self.TWILIO_TOKEN = YOUR TWILIO TOKEN
        self.FROM_NUMBER = SENDER NUMBER
        self.TO_NUMBER = RECEPIENT NUMBER

class EmailInfo:
    def __init__(self):
        self.EMAIL = YOUR EMAIL
        self.PASSWORD = YOUR EMAIL PASSWORD


# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Class Responsible for Getting and Putting Data in Google Sheets ~~~~~~~~~~~~~~~~~~~~~~~~~~
class DataManager:
    def __init__(self):
        self.GoogleInfo = GoogleSheetInfo()
        self.CuttlyInfo = CuttlyINFO()

    def get_data(self, tab_name):
        """A method that acquires and returns needed data from provided Google Sheet."""
        range = f"{tab_name}!A:D"
        response = requests.get(f"{self.GoogleInfo.GOOGLE_SHEETS_ENDPOINT}/{self.GoogleInfo.GOOGLE_SHEET_ID}/values/{range}",
                                headers=self.GoogleInfo.GOOGLE_SHEETS_HEADING)
        response.raise_for_status()

        sheet_raw_data = response.json()["values"]

        if tab_name == "prices":
            sheet_data = []
            for item in sheet_raw_data:
                if item[0] != "City":
                    city = {}
                    city["City"] = item[0]
                    city["IATA Code"] = item[1]
                    city["Lowest Price"] = int(item[2])
                    sheet_data.append(city)
            return sheet_data
        else:
            user_data = []
            for item in sheet_raw_data:
                if item[0] != "First Name":
                    user = {}
                    user["First Name"] = item[0]
                    user["Last Name"] = item[1]
                    user["Email"] = item[2]
                    user_data.append(user)
            return user_data


    def put_data(self, values, range, majorDimension):
        """A method that uploads specific data back onto the Google Sheet."""
        new_values = []
        new_values.append(values)

        range_name = range

        google_sheet_param = {
            "range": range_name,
            "majorDimension": majorDimension,
            "values": new_values
            }

        response = requests.put(f"{self.GoogleInfo.GOOGLE_SHEETS_ENDPOINT}/{self.GoogleInfo.GOOGLE_SHEET_ID}/values/{range_name}?valueInputOption=USER_ENTERED",
                                    headers=self.GoogleInfo.GOOGLE_SHEETS_HEADING, json=google_sheet_param)
        response.raise_for_status()

    def shorten_link(self, link):
        """A method that shortens the provided link."""
        parametars = {
            "key": self.CuttlyInfo.CUTTLY_KEY,
            "short": link,
        }

        response = requests.get(self.CuttlyInfo.CUTTLY_ENDPOINT, params=parametars)
        response.raise_for_status()

        link = response.json()["url"]["shortLink"]

        return link

