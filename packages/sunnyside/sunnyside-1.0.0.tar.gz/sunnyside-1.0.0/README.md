# Sunnyside

[![GitHub release](https://img.shields.io/github/v/release/junqili259/Sunnyside?include_prereleases)](https://github.com/junqili259/Sunnyside/releases)
[![Github all releases](https://img.shields.io/github/downloads/junqili259/Sunnyside/total)](https://github.com/junqili259/Sunnyside/releases)
![Python Version](https://img.shields.io/pypi/pyversions/sunnyside)

## Installation
```
pip3 install sunnyside
```

## Getting Started
### Python Version
Sunnyside only supports python 3.6+
_________________________________________________________________________________________________________________________________________________________________________________

## Current Weather
https://openweathermap.org/current

### Weather by city name
**Note**: Units are by default in Kelvin, to change units to imperial or celsius.
This works for all Current Weather methods.
```python
response = ref.get_current_weather_by_city_name("some_city_name_here","imperial")
```

```python
import sunnyside

ref = sunnyside.CurrentWeather("YOUR-API-KEY-HERE") # Enter your api key here
response = ref.get_current_weather_by_city_name("city_name") # Enter your city name here
```
### Weather by city id
```python
ref.get_current_weather_by_city_id("city_id")
```
### Weather by coordinates 
```python
ref.get_current_weather_by_geo_coords("lat","lon")
```
### Weather by zip code
```python
ref.get_current_weather_by_zip_code("zipcode")
```

_________________________________________________________________________________________________________________________________________________________________________________
## 5 Day Weather Forecast
https://openweathermap.org/forecast5

### Weather by city name
**Note**: Units are by default in Kelvin, to change units to imperial or celsius.
This works for all Current Weather methods.
```python
response = ref.get_forecast_by_city_name("some_city_name_here","imperial")
```

```python
import sunnyside

ref = sunnyside.CurrentWeather("YOUR-API-KEY-HERE") # Enter your api key here
response = ref.get_forecast_by_city_name("city_name") # Enter your city name here
```
### Weather by city id
```python
ref.get_forecast_by_city_id("city_id")
```
### Weather by coordinates 
```python
ref.get_forecast_by_geo_coords("lat","lon")
```
### Weather by zip code
```python
ref.get_forecast_by_zip_code("zipcode")
```

_________________________________________________________________________________________________________________________________________________________________________________

## Reference
https://openweathermap.org/api

https://openweathermap.org/current

https://openweathermap.org/forecast5
