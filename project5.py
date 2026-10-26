"""
╔══════════════════════════════════════════════════════════╗
║              🌤️  Weather App 2026  🌤️                   ║
║         Live Weather via OpenWeatherMap REST API         ║
╚══════════════════════════════════════════════════════════╝

Usage:
    python project5.py

Requirements:
    pip install requests python-dotenv

API Key:
    Get your FREE API key at: https://openweathermap.org/api
    Add it to the .env file:  OPENWEATHER_API_KEY=your_key_here
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────
#  CONFIGURATION  –  Loaded from .env file
# ─────────────────────────────────────────────────────────────
load_dotenv()  # reads .env from the project directory

API_KEY  = os.getenv("OPENWEATHER_API_KEY", "")
UNITS    = os.getenv("UNITS", "metric")   # "metric" = °C | "imperial" = °F
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────

def get_weather(city: str) -> dict:
    """
    Fetch current weather data for a given city from OpenWeatherMap.

    Returns a parsed dict of weather details on success.
    Raises a descriptive RuntimeError on any failure.
    """
    if not city.strip():
        raise ValueError("City name cannot be empty.")

    params = {
        "q":     city.strip(),
        "appid": API_KEY,
        "units": UNITS,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "❌ Network error: Could not connect to the weather service.\n"
            "   Please check your internet connection and try again."
        )
    except requests.exceptions.Timeout:
        raise RuntimeError(
            "❌ Request timed out. The weather service is taking too long.\n"
            "   Please try again in a moment."
        )
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"❌ Unexpected network error: {exc}")

    # Handle HTTP-level errors
    if response.status_code == 401:
        raise RuntimeError(
            "❌ Invalid API key. Please check your API_KEY in project5.py.\n"
            "   Get a free key at: https://openweathermap.org/api"
        )
    elif response.status_code == 404:
        raise RuntimeError(
            f"❌ City '{city}' not found. Please check the spelling and try again."
        )
    elif response.status_code == 429:
        raise RuntimeError(
            "❌ API rate limit exceeded. Please wait a minute before retrying."
        )
    elif response.status_code != 200:
        raise RuntimeError(
            f"❌ Weather service returned an error (HTTP {response.status_code}).\n"
            f"   Response: {response.text}"
        )

    data = response.json()

    # Parse and return only what we need
    return {
        "city":        data["name"],
        "country":     data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like":  data["main"]["feels_like"],
        "temp_min":    data["main"]["temp_min"],
        "temp_max":    data["main"]["temp_max"],
        "humidity":    data["main"]["humidity"],
        "pressure":    data["main"]["pressure"],
        "condition":   data["weather"][0]["main"],
        "description": data["weather"][0]["description"].title(),
        "wind_speed":  data["wind"]["speed"],
        "wind_deg":    data["wind"].get("deg", "N/A"),
        "visibility":  data.get("visibility", "N/A"),
        "sunrise":     data["sys"]["sunrise"],
        "sunset":      data["sys"]["sunset"],
        "timezone":    data["timezone"],
    }


def condition_emoji(condition: str) -> str:
    """Return an emoji that matches the weather condition."""
    mapping = {
        "Clear":         "☀️ ",
        "Clouds":        "☁️ ",
        "Rain":          "🌧️ ",
        "Drizzle":       "🌦️ ",
        "Thunderstorm":  "⛈️ ",
        "Snow":          "❄️ ",
        "Mist":          "🌫️ ",
        "Smoke":         "🌫️ ",
        "Haze":          "🌫️ ",
        "Dust":          "🌪️ ",
        "Fog":           "🌫️ ",
        "Sand":          "🌪️ ",
        "Ash":           "🌋 ",
        "Squall":        "💨 ",
        "Tornado":       "🌪️ ",
    }
    return mapping.get(condition, "🌡️ ")


def wind_direction(deg) -> str:
    """Convert wind degrees to a compass direction."""
    if deg == "N/A":
        return "N/A"
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(deg / 22.5) % 16
    return directions[index]


def format_time(unix_ts: int, tz_offset: int) -> str:
    """Convert a UTC Unix timestamp + timezone offset to a local HH:MM string."""
    local_ts = unix_ts + tz_offset
    return datetime.utcfromtimestamp(local_ts).strftime("%H:%M")


def display_weather(w: dict) -> None:
    """Print a nicely formatted weather report."""
    unit_symbol = "°C" if UNITS == "metric" else "°F"
    speed_unit  = "m/s" if UNITS == "metric" else "mph"
    emoji       = condition_emoji(w["condition"])
    wind_dir    = wind_direction(w["wind_deg"])
    sunrise     = format_time(w["sunrise"], w["timezone"])
    sunset      = format_time(w["sunset"],  w["timezone"])
    visibility  = (f"{w['visibility'] / 1000:.1f} km"
                   if isinstance(w["visibility"], int) else "N/A")

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print(f"║  {emoji} Weather Report — {w['city']}, {w['country']:<35}║")
    print("╠══════════════════════════════════════════════════════════╣")
    print(f"║  Condition    : {w['description']:<41}║")
    print(f"║  Temperature  : {w['temperature']}{unit_symbol}  (feels like {w['feels_like']}{unit_symbol}){'':<11}║")
    print(f"║  High / Low   : {w['temp_max']}{unit_symbol}  /  {w['temp_min']}{unit_symbol}{'':<20}║")
    print(f"║  Humidity     : {w['humidity']}%{'':<40}║")
    print(f"║  Pressure     : {w['pressure']} hPa{'':<37}║")
    print(f"║  Wind         : {w['wind_speed']} {speed_unit}  {wind_dir:<37}║")
    print(f"║  Visibility   : {visibility:<41}║")
    print(f"║  Sunrise      : {sunrise:<41}║")
    print(f"║  Sunset       : {sunset:<41}║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()


# ─────────────────────────────────────────────────────────────
#  MAIN  –  Interactive loop
# ─────────────────────────────────────────────────────────────

def main():
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║            🌤️   W E A T H E R   A P P   2 0 2 6  🌤️    ║")
    print("║         Live weather powered by OpenWeatherMap           ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # Warn if no API key is configured
    if not API_KEY or API_KEY == "your_api_key_here":
        print()
        print("  ⚠️  WARNING: No API key found.")
        print("     Open .env and set:  OPENWEATHER_API_KEY=your_real_key")
        print("     Free key → https://openweathermap.org/api")
        print()

    while True:
        try:
            print("  Enter a city name (or 'quit' to exit):")
            city = input("  > ").strip()

            if city.lower() in {"quit", "exit", "q"}:
                print()
                print("  👋  Thanks for using Weather App 2026. Goodbye!")
                print()
                sys.exit(0)

            weather_data = get_weather(city)
            display_weather(weather_data)

        except ValueError as exc:
            # Empty input
            print(f"\n  ⚠️  {exc}\n")

        except RuntimeError as exc:
            # API / network errors (already contain ❌ prefix)
            print(f"\n{exc}\n")

        except KeyboardInterrupt:
            print()
            print("\n  👋  Interrupted. Goodbye!")
            print()
            sys.exit(0)


if __name__ == "__main__":
    main()
