import pytest
from httpx import HTTPStatusError, Response
from weather.clients.openweather_impl import OpenWeatherClient

@pytest.fixture
def openweather_client():
    return OpenWeatherClient(api_key="test_api_key")

@pytest.mark.asyncio
async def test_get_weather_success(mocker, openweather_client):
    mock_response = mocker.Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"daily": [{"temp": {"max": 25, "min": 15}, "weather": [{"description": "clear sky"}]}]}
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)
    result = await openweather_client.get_weather(latitude=19.4326, longitude=-99.1332)
    assert result == {"daily": [{"temp": {"max": 25, "min": 15}, "weather": [{"description": "clear sky"}]}]}

@pytest.mark.asyncio
async def test_get_weather_http_error(mocker, openweather_client):
    mock_response = mocker.Mock(spec=Response)
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = HTTPStatusError("HTTP error", request=None, response=mock_response)
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)
    result = await openweather_client.get_weather(latitude=19.4326, longitude=-99.1332)
    assert result == {}

@pytest.mark.asyncio
async def test_get_weather_unknown_error(mocker, openweather_client):
    mocker.patch("httpx.AsyncClient.get", side_effect=Exception("Unknown error"))
    result = await openweather_client.get_weather(latitude=19.4326, longitude=-99.1332)
    assert result == {}
