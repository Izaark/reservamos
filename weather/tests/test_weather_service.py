from unittest.mock import patch, AsyncMock
import pytest
from weather.services.weather_service_impl import WeatherService
from weather.clients.openweather_impl import OpenWeatherClient
from weather.services.services_constants import CACHE_TIME_OUT_FORECAST

@pytest.fixture
def mock_openweather_client():
    return AsyncMock(spec=OpenWeatherClient)

@pytest.fixture
def weather_service(mock_openweather_client):
    return WeatherService(openweather_client=mock_openweather_client)

@pytest.mark.asyncio
async def test_get_weather_forecast_no_cache(weather_service, mock_openweather_client):
    mock_openweather_client.get_weather.return_value = {
        "daily": [
            {"dt": 1634056800, "temp": {"max": 25.0, "min": 15.0}, "weather": [{"description": "clear sky"}]},
            {"dt": 1634143200, "temp": {"max": 22.0, "min": 14.0}, "weather": [{"description": "partly cloudy"}]}
        ]
    }
    city_list = [{"name": "Ciudad de México", "latitude": 19.4326, "longitude": -99.1332}]
    
    with patch("django.core.cache.cache.get", return_value=None) as mock_cache_get, \
         patch("django.core.cache.cache.set") as mock_cache_set:
        
        result = await weather_service.get_weather_forecast(city_list)
        expected_result = [
            [
                {"date": "2021-10-12", "temperature_max": 25.0, "temperature_min": 15.0, "weather": "clear sky"},
                {"date": "2021-10-13", "temperature_max": 22.0, "temperature_min": 14.0, "weather": "partly cloudy"}
            ]
        ]
        
        assert result == expected_result
        mock_cache_set.assert_called_once_with("weather_forecast_19.4326_-99.1332", expected_result[0], timeout=CACHE_TIME_OUT_FORECAST)

@pytest.mark.asyncio
async def test_get_weather_forecast_with_cache(weather_service):
    cached_data = [
        {"date": "2021-10-12", "temperature_max": 25.0, "temperature_min": 15.0, "weather": "clear sky"}
    ]
    city_list = [{"name": "Ciudad de México", "latitude": 19.4326, "longitude": -99.1332}]
    
    with patch("django.core.cache.cache.get", return_value=cached_data) as mock_cache_get:
        result = await weather_service.get_weather_forecast(city_list)
        assert result == [cached_data]
        weather_service.openweather_client.get_weather.assert_not_called()

@pytest.mark.asyncio
async def test_get_weather_forecast_empty_response(weather_service, mock_openweather_client):
    mock_openweather_client.get_weather.return_value = {}
    city_list = [{"name": "Ciudad de México", "latitude": 19.4326, "longitude": -99.1332}]
    
    with patch("django.core.cache.cache.get", return_value=None) as mock_cache_get, \
         patch("django.core.cache.cache.set") as mock_cache_set:
        
        result = await weather_service.get_weather_forecast(city_list)
        assert result == [[]]
        mock_cache_set.assert_called_once_with("weather_forecast_19.4326_-99.1332", [], timeout=CACHE_TIME_OUT_FORECAST)

def test_build_daily_forecast(weather_service):
    weather_data = {
        "daily": [
            {"dt": 1727839969, "temp": {"max": 25.0, "min": 15.0}, "weather": [{"description": "clear sky"}]},
            {"dt": 1727926369, "temp": {"max": 22.0, "min": 14.0}, "weather": [{"description": "partly cloudy"}]}
        ]
    }
    expected_result = [
        {"date": "2024-10-02", "temperature_max": 25.0, "temperature_min": 15.0, "weather": "clear sky"},
        {"date": "2024-10-03", "temperature_max": 22.0, "temperature_min": 14.0, "weather": "partly cloudy"}
    ]
    result = weather_service._build_daily_forecast(weather_data)
    assert result == expected_result

def test_convert_unix_to_date(weather_service):
    unix_timestamp = 1727839969
    result = weather_service._convert_unix_to_date(unix_timestamp)
    assert result == "2024-10-02"
