import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_current_weather(location_query="Yogyakarta"):
    """
    Fetches current weather data from OpenWeatherMap.
    Accepts specific city name (e.g. "Sleman, ID") or defaults.
    """
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "your_openweather_api_key_here":
        return "Data cuaca tidak tersedia (API Key missing)."

    try:
        # Check if input looks like coordinates (lat,lon)
        if "," in location_query and any(char.isdigit() for char in location_query.split(",")[0]):
             # Simple heuristic for "lat,lon" vs "City, Country"
             # If it works, great. If not, API will handle or fail.
             # Actually, simpler to just treat as query 'q' for text, or direct url if we want.
             # OpenWeather 'q' parameter handles "City" or "City,Country".
             url = f"{BASE_URL}?q={location_query}&appid={OPENWEATHER_API_KEY}&units=metric&lang=id"
        else:
             # Assume City Name
             url = f"{BASE_URL}?q={location_query}&appid={OPENWEATHER_API_KEY}&units=metric&lang=id"

        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            city_name = data.get('name', location_query)
            
            return f"Lokasi: {city_name} | Kondisi: {description}, Suhu: {temp}°C, Kelembapan: {humidity}%"
        else:
            return f"Gagal mengambil data cuaca: {data.get('message', 'Unknown error')}"
            
    except Exception as e:
        return f"Error koneksi cuaca: {str(e)}"
