import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

class WeatherClient:
    def __init__(self):
        # Setup the Open-Meteo API client with cache and retry on error
        self.cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
        self.retry_session = retry(self.cache_session, retries = 5, backoff_factor = 0.2)
        self.openmeteo = openmeteo_requests.Client(session = self.retry_session)

    def get_historical_weather(self, lat: float, lon: float, start_date: str, end_date: str) -> pd.DataFrame:
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ["temperature_2m", "wind_speed_100m", "shortwave_radiation"]
        }
        
        responses = self.openmeteo.weather_api(url, params=params)
        response = responses[0]
        
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_wind_speed_100m = hourly.Variables(1).ValuesAsNumpy()
        hourly_shortwave_radiation = hourly.Variables(2).ValuesAsNumpy()
        
        # Calculate timestamps
        # TimeEnd could be one interval past the last data point, depending on the response
        time_index = pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )
        
        df = pd.DataFrame({
            "timestamp": time_index,
            "temperature_2m": hourly_temperature_2m,
            "wind_speed_100m": hourly_wind_speed_100m,
            "solar_radiation_ghi": hourly_shortwave_radiation
        })
        
        return df
