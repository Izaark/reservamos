# Weather API

Weather API that allows to get weather information for different cities using OpenWeather and Reservamos API.

## Architecture

- **Views (Controllers)**:
  - Handle HTTP requests and communicate with services.

- **Services (CityService, WeatherService)**:
  - Handle business logic.
  - Interact with clients (external APIs).
  - Implement interfaces to decouple logic and dependencies.

- **Clients (ReservamosClient, OpenWeatherClient)**:
  - Manage communication with external APIs.
  - Implement interfaces to support different data providers.

- **Dependency Container**:
  - Manages service and client dependencies.
  - Injects the appropriate implementations into each component.

- **Caching Layer**:
  - Used to store API responses and improve performance.

### Communication Flow:
- **Views** ⟶ **Services** ⟶ **Clients** ⟶ **External APIs**
- **Services** ⟶ **Caching Layer** (to optimize calls and results)

## Setup

## 1. Clone the Repository

```bash
git clone https://github.com/Izaark/reservamos.git
cd reservamos
```

## 2. Create the `.env` File

Create a `.env` file in the root directory with the following content:

```env
DJANGO_SECRET_KEY={SECRET_KEY}
DJANGO_ALLOWED_HOSTS={HOST}
OPENWEATHER_API_KEY={API_KEY}
```

## 3. Build the Docker Image

```bash
docker build -t weather-api .
```

## 4. Run the Docker Container

```bash
docker run -d -p 8000:8000 --name weather-container --env-file .env weather-api
```

## 5. Access the Application

The API provides weather forecasts for cities in Mexico using data from OpenWeather and Reservamos APIs.

### 5.1 API Endpoints

- **Local Base URL**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Production Base URL**: [https://reservamos-production.up.railway.app](https://reservamos-production.up.railway.app)

### 5.2 Forecast Endpoint

The primary endpoint is `/api/forecast/`, which returns the 7-day weather forecast for a specified city:

- **Request Format**: `/api/forecast/?city=<city_name>`
- **Example Request**: 
  - [http://127.0.0.1:8000/api/forecast/?city=cdmx](http://127.0.0.1:8000/api/forecast/?city=cdmx)
  - [https://reservamos-production.up.railway.app/api/forecast/?city=cdmx](https://reservamos-production.up.railway.app/api/forecast/?city=cdmx)

### 5.3 Request Parameters

- `city` (required): Partial or full city name (e.g., `cdmx` or `Monterrey`).

### 5.4 Response Format

The response is a JSON object containing the weather forecast for the matched cities:

```json
{
    "results": [
        {	
			"state": "Distrito Federal",
			"city": "Mexico City",
            "forecast": [
                {"date": "2024-10-04", "temperature_max": 23.1, "temperature_min": 15.0, "weather": "scattered clouds"},
                {"date": "2024-10-05", "temperature_max": 22.5, "temperature_min": 14.8, "weather": "light rain"}
            ]
        }
    ]
}
```

### 5.5 Error Handling
- 400 Bad Request: No city name provided.
- 404 Not Found: No cities found matching the query.
- 500 Internal Server Error: Unexpected server error during API calls.

## 6. Running Unit Tests

To run the unit tests, use the following command:

```bash
docker exec -it weather-container pytest
```


### 6.1 Viewing Coverage Report

Generate the Coverage Report:

```bash
docker exec -it weather-container coverage run -m pytest
```

View the Coverage Report in the Terminal:

```bash
docker exec -it weather-container coverage report
```


### Additional Commands

- **Stop the Container**: `docker stop weather-container`
- **Remove the Container**: `docker rm weather-container`
- **Remove the Image**: `docker rmi weather-api`
- **Run Tests**: `docker exec -it weather-container pytest`
- **View Logs**: `docker logs weather-container`


