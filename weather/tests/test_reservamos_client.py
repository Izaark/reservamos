
import pytest
from httpx import HTTPStatusError, Response
from weather.clients.reservamos_impl import ReservamosClient

@pytest.fixture
def reservamos_client():
    return ReservamosClient()

@pytest.mark.asyncio
async def test_get_cities_success(mocker, reservamos_client):
    mock_response = mocker.Mock(spec=Response)
    mock_response.status_code = 201
    mock_response.json.return_value = [
        {"display": "Ciudad de México", "lat": 19.4326, "long": -99.1332, "country": "México"},
        {"display": "Monterrey", "lat": 25.6866, "long": -100.3161, "country": "México"}
    ]
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)
    result = await reservamos_client.get_cities("mexico")
    expected_result = [
        {"display": "Ciudad de México", "lat": 19.4326, "long": -99.1332, "country": "México"},
        {"display": "Monterrey", "lat": 25.6866, "long": -100.3161, "country": "México"}
    ]
    assert result == expected_result

@pytest.mark.asyncio
async def test_get_cities_http_error(mocker, reservamos_client):
    mock_response = mocker.Mock(spec=Response)
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = HTTPStatusError("HTTP error", request=None, response=mock_response)
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)
    result = await reservamos_client.get_cities("invalid_city")
    assert result is None

@pytest.mark.asyncio
async def test_get_cities_unknown_error(mocker, reservamos_client):
    mocker.patch("httpx.AsyncClient.get", side_effect=Exception("Unknown error"))
    result = await reservamos_client.get_cities("unknown_error")
    assert result is None
