import logging
from django.http import JsonResponse, HttpRequest
from weather.services.city_service import ICityService, CityList
from weather.services.weather_service import IWeatherService, ForecastList
from weather.inject_container import container


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class WeatherForecastView:
    def __init__(self, city_service: ICityService, weather_service: IWeatherService) -> None:
        self.city_service = city_service
        self.weather_service = weather_service

    async def get_weather_forecast(self, request: HttpRequest) -> JsonResponse:
        city_name = request.GET.get("city", "")
        if not city_name:
            return JsonResponse({"error": "No city name provided."}, status=400)

        cities = await self._get_city_coordinates(city_name)
        if not cities:
            logger.error("No cities found for the given name.")
            return JsonResponse({"error": "No cities found for the given name."}, status=404)

        forecasts = await self._get_weather_forecast(cities)
        return self._build_response(cities, forecasts)
        
    async def _get_city_coordinates(self, city_name: str) -> CityList:
        try:
            return await self.city_service.get_city_coordinates(city_name)
        except Exception as e:
            logger.error(f"Error getting city coordinates from {city_name}: {e}")
            return None

    async def _get_weather_forecast(self, cities: CityList) -> ForecastList:
        try:
            return await self.weather_service.get_weather_forecast(cities)
        except Exception as e:
            logger.error(f"Error getting forecast: {e}")
            return []
        
    def _build_response(self, cities: CityList, forecasts: ForecastList) -> JsonResponse:
        results = [
            {
                "state": city["state"],
                "city": city["name"],
                "forecast": forecast
            }
            for city, forecast in zip(cities, forecasts)
        ]
        return JsonResponse({"results": results})


weather_forecast_view = WeatherForecastView(
    city_service=container.get_city_service(),
    weather_service=container.get_weather_service()
)

async def weather_forecast(request):
    return await weather_forecast_view.get_weather_forecast(request)
