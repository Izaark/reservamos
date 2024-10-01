from unittest.mock import patch, AsyncMock
import pytest
from weather.services.city_service_impl import CityService
from weather.clients.reservamos_impl import ReservamosClient
from weather.services.services_constants import CACHE_TIME_OUT_CITY

@pytest.fixture
def mock_reservamos_client():
    return AsyncMock(spec=ReservamosClient)

@pytest.fixture
def city_service(mock_reservamos_client):
    return CityService(reservamos_client=mock_reservamos_client)

@pytest.mark.asyncio
async def test_get_city_coordinates_with_cache(city_service):
    cached_data = [
        {"name": "Ciudad de México", "latitude": 19.4326, "longitude": -99.1332}
    ]
    with patch("django.core.cache.cache.get", return_value=cached_data) as mock_cache_get:
        result = await city_service.get_city_coordinates("cdmx")
        assert result == cached_data
        city_service.reservamos_client.get_cities.assert_not_called()
        mock_cache_get.assert_called_once_with("city_coordinates_cdmx")

@pytest.mark.asyncio
async def test_get_city_coordinates_empty_response(city_service, mock_reservamos_client):
    mock_reservamos_client.get_cities.return_value = []
    with patch("django.core.cache.cache.get", return_value=None) as mock_cache_get, \
         patch("django.core.cache.cache.set") as mock_cache_set:
        result = await city_service.get_city_coordinates("unknown_city")
        assert result == []
        mock_cache_set.assert_called_once_with("city_coordinates_unknown_city", [], timeout=CACHE_TIME_OUT_CITY)
        mock_cache_get.assert_called_once_with("city_coordinates_unknown_city")

def test_build_cities(city_service):
    places = [
        {"display": "Ciudad de México", "lat": 19.4326, "long": -99.1332, "result_type": "city"},
        {"display": "Monterrey", "lat": 25.6866, "long": -100.3161, "result_type": "city"},
        {"display": "Tijuana", "lat": None, "long": None, "result_type": "city"},
        {"display": "Non-City Place", "lat": 22.5726, "long": 88.3639, "result_type": "terminal"}
    ]
    expected_result = [
        {"name": "Ciudad de México", "latitude": 19.4326, "longitude": -99.1332},
        {"name": "Monterrey", "latitude": 25.6866, "longitude": -100.3161}
    ]
    
    result = city_service._build_cities(places)
    assert result == expected_result
