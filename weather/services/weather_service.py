from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, TypeAlias
from weather.services.city_service import CityList

WeatherData: TypeAlias = Dict[str, Any]
ForecastList: TypeAlias = Optional[List[WeatherData]]

class IWeatherService(ABC):
    @abstractmethod
    async def get_weather_forecast(self, cities: CityList) -> ForecastList:
        pass 
