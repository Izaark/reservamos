from datetime import datetime, timezone
from typing import List
import asyncio
from django.core.cache import cache
from weather.clients.openweather import IOpenWeatherClient
from weather.services.weather_service import IWeatherService, ForecastList, WeatherData
from weather.services.city_service import CityList
from weather.services.services_constants import CACHE_TIME_OUT_FORECAST

class WeatherService(IWeatherService):
    def __init__(self, openweather_client: IOpenWeatherClient) -> None:
        self.openweather_client = openweather_client
    
    async def get_weather_forecast(self, cities: CityList) -> ForecastList:
        tasks = [
            self._get_daily_forecast(city["latitude"], city["longitude"])
            for city in cities
        ]
        return await asyncio.gather(*tasks)
        
    async def _get_daily_forecast(self, latitude: float, longitude: float) -> ForecastList:
        daily_forecast = self._get_cached_forecast(latitude, longitude)
        if daily_forecast is None:
                weather_data = await self.openweather_client.get_weather(latitude, longitude)
                daily_forecast = self._build_daily_forecast(weather_data)
                self._set_cache_forecast(latitude, longitude, daily_forecast)
        return daily_forecast
    
    def _get_cached_forecast(self, latitude: float, longitude: float) -> ForecastList:
        cache_key = f"weather_forecast_{latitude}_{longitude}"
        return cache.get(cache_key)

    def _set_cache_forecast(self, latitude: float, longitude: float, daily_forecast) -> None:
        cache_key = f"weather_forecast_{latitude}_{longitude}"
        cache.set(cache_key, daily_forecast, timeout=CACHE_TIME_OUT_FORECAST)
        
    def _convert_unix_to_date(self, unix_timestamp: int) -> str:
        date_obj = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
        return date_obj.strftime('%Y-%m-%d')

    def _build_daily_forecast(self, weather_data: WeatherData) -> List[WeatherData]:
        return [
            {
                "date": self._convert_unix_to_date(day["dt"]),
                "temperature_max": day["temp"]["max"],
                "temperature_min": day["temp"]["min"],
                "weather": day["weather"][0]["description"],
            }
            for day in weather_data.get("daily", [])
        ]