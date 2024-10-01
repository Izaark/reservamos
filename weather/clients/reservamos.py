from abc import ABC, abstractmethod
from typing import List, Dict, Any, TypeAlias, Optional


CityData: TypeAlias = Dict[str, Any] 
CityListResponse: TypeAlias = Optional[List[CityData]]

class IReservamosClient(ABC):
    @abstractmethod
    async def get_cities(self, city_name: str) -> CityListResponse:
        pass