import os
from dotenv import load_dotenv
from weather.clients.reservamos_impl import ReservamosClient
from weather.clients.openweather_impl import OpenWeatherClient
from weather.services.city_service_impl import CityService
from weather.services.weather_service_impl import WeatherService


load_dotenv()

class InjectContainer:
    def __init__(self):
        openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
        if not openweather_api_key:
            raise ValueError("OPENWEATHER_API_KEY environment variable is missing.")
        
        self.reservamos_client = ReservamosClient()
        self.openweather_client = OpenWeatherClient(api_key=openweather_api_key)

        self.city_service = CityService(self.reservamos_client)
        self.weather_service = WeatherService(self.openweather_client)

    def get_city_service(self):
        return self.city_service

    def get_weather_service(self):
        return self.weather_service

container = InjectContainer()
