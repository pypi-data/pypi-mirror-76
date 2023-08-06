from .currentWeather import CurrentWeather
from .fiveDayForecast import FiveDayForecast


class Sunnyside:
    def __init__(self, api_key, units= None):
        self.api_key = api_key
        self.units = units
    
    def currentWeather(self):
        return CurrentWeather(self.api_key, self.units)

    def fiveDayForecast(self):
        return FiveDayForecast(self.api_key, self.units)