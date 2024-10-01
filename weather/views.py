import logging
from django.http import JsonResponse
from weather.inject_container import container


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class WeatherForecastView:
    def __init__(self, city_service, weather_service):
        self.city_service = city_service
        self.weather_service = weather_service

    async def get_weather_forecast(self, request):
        city_name = request.GET.get("city", "")
        if not city_name:
            return JsonResponse({"error": "No city name provided."}, status=400)

        cities = await self._get_city_coordinates(city_name)
        if not cities:
            logger.error("No cities found for the given name.")
            return JsonResponse({"error": "No cities found for the given name."}, status=404)

        forecasts = await self._get_weather_forecast(cities)
        return self._build_response(cities, forecasts)
        
    async def _get_city_coordinates(self, city_name: str):
        try:
            return await self.city_service.get_city_coordinates(city_name)
        except Exception as e:
            logger.error(f"Error getting city coordinates from {city_name}: {e}")
            return None

    async def _get_weather_forecast(self, cities):
        try:
            return await self.weather_service.get_weather_forecast(cities)
        except Exception as e:
            logger.error(f"Error getting forecast: {e}")
            return []
        
    def _build_response(self, cities, forecasts):
        results = [
            {
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
