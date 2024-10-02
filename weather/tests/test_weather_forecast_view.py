import pytest
from unittest.mock import AsyncMock, Mock
from django.http import JsonResponse
from weather.views import WeatherForecastView, weather_forecast

@pytest.fixture
def mock_city_service():
    return AsyncMock()

@pytest.fixture
def mock_weather_service():
    return AsyncMock()

@pytest.fixture
def weather_forecast_view_instance(mock_city_service, mock_weather_service):
    return WeatherForecastView(city_service=mock_city_service, weather_service=mock_weather_service)

@pytest.mark.asyncio
async def test_get_weather_forecast_success(mocker, weather_forecast_view_instance, mock_city_service, mock_weather_service):
    mock_city_service.get_city_coordinates.return_value = [
        {"name": "Ciudad de México", "latitude": 19.4326, "longitude": -99.1332, "state": "DF"}
    ]
    mock_weather_service.get_weather_forecast.return_value = [
        [
            {"date": "2024-10-02", "temperature_max": 25.0, "temperature_min": 15.0, "weather": "clear sky"},
            {"date": "2024-10-03", "temperature_max": 22.0, "temperature_min": 14.0, "weather": "partly cloudy"}
        ]
    ]
    mock_request = Mock()
    mock_request.GET = {"city": "mexico"}
    response = await weather_forecast_view_instance.get_weather_forecast(mock_request)
    
    expected_response = JsonResponse({
        "results": [
            {   
                "state": "DF",
                "city": "Ciudad de México",
                "forecast": [
                    {"date": "2024-10-02", "temperature_max": 25.0, "temperature_min": 15.0, "weather": "clear sky"},
                    {"date": "2024-10-03", "temperature_max": 22.0, "temperature_min": 14.0, "weather": "partly cloudy"}
                ]
            }
        ]
    })

    assert response.status_code == 200
    assert response.content == expected_response.content

@pytest.mark.asyncio
async def test_get_weather_forecast_no_city_provided(weather_forecast_view_instance):
    mock_request = Mock()
    mock_request.GET = {}
    response = await weather_forecast_view_instance.get_weather_forecast(mock_request)
    expected_response = JsonResponse({"error": "No city name provided."}, status=400)

    assert response.status_code == 400
    assert response.content == expected_response.content

@pytest.mark.asyncio
async def test_get_weather_forecast_city_not_found(weather_forecast_view_instance, mock_city_service):
    mock_city_service.get_city_coordinates.return_value = None
    mock_request = Mock()
    mock_request.GET = {"city": "invalid_city"}
    response = await weather_forecast_view_instance.get_weather_forecast(mock_request)
    expected_response = JsonResponse({"error": "No cities found for the given name."}, status=404)

    assert response.status_code == 404
    assert response.content == expected_response.content