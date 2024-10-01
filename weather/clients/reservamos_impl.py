import logging
import httpx
from weather.clients.reservamos import IReservamosClient, CityListResponse


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ReservamosClient(IReservamosClient):
    BASE_URL = "https://search.reservamos.mx/api/v2/places"

    async def get_cities(self, city_name: str) -> CityListResponse:
        url: str = f"{self.BASE_URL}?q={city_name}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

            if response.status_code == 201:
                return response.json()
            else:
                logger.warning(f"Request to Reservamos API failed for {city_name}: Status Code {response.status_code}")
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error when requesting {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unknown error when requesting {url} with city '{city_name}': {e}")
            return None
