import requests

class FiveDayForecast:
    def __init__(self, api_key, units = None):
        self.api_key = api_key
        self.units = units

    def get_forecast_by_city_name(self, city_name):
        if self.units == None:
            api_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={self.api_key}"
        else:
            api_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={self.api_key}" + f"&units={self.units}"

        response = requests.get(url=api_url)
        return response.json()

    def get_forecast_by_city_id(self, city_id):
        if self.units == None:
            api_url = f"https://api.openweathermap.org/data/2.5/forecast?id={city_id}&appid={self.api_key}"
        else:
            api_url = f"https://api.openweathermap.org/data/2.5/forecast?id={city_id}&appid={self.api_key}" + f"&units={self.units}"

        response = requests.get(url=api_url)
        return response.json()

    def get_forecast_by_geo_coords(self, lat, lon):
        if self.units == None:
            api_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}"
        else:
            api_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}" + f"&units={self.units}"

        response = requests.get(url=api_url)
        return response.json()
    
    def get_forecast_by_zip_code(self, zip_code, country_code="us"):
        if self.units == None:
            api_url = f"api.openweathermap.org/data/2.5/forecast?zip={zip_code},{country_code}&appid={self.api_key}"
        else:
            api_url = f"api.openweathermap.org/data/2.5/forecast?zip={zip_code},{country_code}&appid={self.api_key}" + f"&units={self.units}"
            
        response = requests.get(url=api_url)
        return response.json()