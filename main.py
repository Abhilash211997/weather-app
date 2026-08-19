import requests


def get_weather(city):
    print()
    print("==============================")
    print("          WEATHER APP")
    print("==============================")
    print()

    # Find the city's coordinates
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    except requests.RequestException:
        print("Error: Could not get city data.")
        return

    # Check if city was found
    if "results" not in data or not data["results"]:
        print("City not found.")
        return

    location = data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    print(f"City: {location['name']}")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")

    # Get weather data
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "auto"
    }

    try:
        weather_response = requests.get(
            weather_url,
            params=weather_params
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

    except requests.RequestException:
        print("Error: Could not get weather data.")
        return

    current_weather = weather_data["current"]

    temperature = current_weather["temperature_2m"]
    humidity = current_weather["relative_humidity_2m"]
    wind_speed = current_weather["wind_speed_10m"]
    weather_code = current_weather["weather_code"]

    # Convert weather code to description
    if weather_code == 0:
        condition = "Clear sky"
    elif weather_code in [1, 2, 3]:
        condition = "Cloudy"
    elif weather_code in [45, 48]:
        condition = "Fog"
    elif weather_code in [51, 53, 55, 56, 57]:
        condition = "Drizzle"
    elif weather_code in [61, 63, 65, 66, 67]:
        condition = "Rain"
    elif weather_code in [71, 73, 75, 77]:
        condition = "Snow"
    elif weather_code in [80, 81, 82]:
        condition = "Rain showers"
    elif weather_code in [95, 96, 99]:
        condition = "Thunderstorm"
    else:
        condition = "Unknown"

    print()
    print("==============================")
    print("          WEATHER APP")
    print("==============================")
    print()
    print(f"City: {location['name']}")
    print(f"Temperature: {temperature} °C")
    print(f"Weather: {condition}")
    print(f"Humidity: {humidity} %")
    print(f"Wind Speed: {wind_speed} km/h")
    print()
    print("==============================")


# Run the program

while True:
    city = input("Enter city name: ").strip()

    get_weather(city)

    again = input("Do you want to check another city? (y/n): ")

    if again.lower() != "y":
        print("Thank you for using the Weather App!")
        break