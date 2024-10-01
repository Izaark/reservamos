from abc import ABC, abstractmethod
from typing import Dict, Any, TypeAlias, Optional 


WeatherData: TypeAlias = Dict[str, Any]
WeatherResponse: TypeAlias = Optional[WeatherData]

class IOpenWeatherClient(ABC):
    @abstractmethod
    async def get_weather(self, latitude: float, longitude: float):
        pass