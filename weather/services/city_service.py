from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, TypeAlias


CityType: TypeAlias = Dict[str, Any]
CityList: TypeAlias = Optional[List[CityType]]

class ICityService(ABC):
    @abstractmethod
    async def get_city_coordinates(self, city_name: str) -> CityList:
        pass 