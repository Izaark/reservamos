from typing import List
from django.core.cache import cache
from weather.clients.reservamos import IReservamosClient
from weather.services.city_service import ICityService, CityList, CityType
from weather.services.services_constants import CACHE_TIME_OUT_CITY


class CityService(ICityService):
    def __init__(self, reservamos_client: IReservamosClient ) -> None:
        self.reservamos_client = reservamos_client
        
    async def get_city_coordinates(self, city_name: str) -> CityList:
        city_list = self._get_cached_city_list(city_name)
        if city_list is None:
            places = await self.reservamos_client.get_cities(city_name)
            city_list = self._build_cities(places)
            self._set_cache_city_list(city_name, city_list)
        return city_list

    def _get_cached_city_list(self, city_name: str) -> CityList:
        cache_key = f"city_coordinates_{city_name}"
        return cache.get(cache_key)

    def _set_cache_city_list(self, city_name: str, city_list: CityList) -> None:
        cache_key = f"city_coordinates_{city_name}"
        cache.set(cache_key, city_list, timeout=CACHE_TIME_OUT_CITY)
        
    def _build_cities(self, places: CityList) -> List[CityType]:
        unique_cities = {
            (place["lat"], place["long"]): {
                "name": place["display"],
                "latitude": place["lat"],
                "longitude": place["long"]
            }
            for place in places
            if place["result_type"] == "city" and place["lat"] is not None and place["long"] is not None
        }
        return list(unique_cities.values())