import logging
import httpx
from weather.clients.openweather import IOpenWeatherClient, WeatherResponse


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OpenWeatherClient(IOpenWeatherClient):
    BASE_URL = "https://api.openweathermap.org/data/2.5/onecall"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def get_weather(self, latitude: float, longitude: float) -> WeatherResponse:
        url = (
            f"{self.BASE_URL}?lat={latitude}&lon={longitude}&exclude=hourly,minutely"
            f"&units=metric&appid={self.api_key}"
        )
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Request to OpenWeather API failed for coordinates (lat: {latitude}, lon: {longitude}): Status Code {response.status_code}")
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error when requesting {url}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unknown error when requesting {url} for coordinates (lat: {latitude}, lon: {longitude}): {e}")
            return {}
