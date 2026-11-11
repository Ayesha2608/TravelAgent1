import requests

def get_weather(place: str) -> dict:
    """Return current conditions and next few days, not historical or long-range forecasts."""
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": place, "count": 1, "language": "en", "format": "json"},
        timeout=12,
    )
    geo.raise_for_status()
    found = geo.json().get("results", [])
    if not found:
        raise ValueError("Location not found. Try a nearby city or a more specific name.")
    loc = found[0]
    result = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": loc["latitude"], "longitude": loc["longitude"],
            "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "timezone": "auto", "forecast_days": 5,
        }, timeout=12,
    )
    result.raise_for_status()
    w = result.json()
    days = []
    for i, date in enumerate(w["daily"]["time"]):
        days.append({
            "date": date,
            "max_c": w["daily"]["temperature_2m_max"][i],
            "min_c": w["daily"]["temperature_2m_min"][i],
            "precipitation_probability_max_percent": w["daily"]["precipitation_probability_max"][i],
        })
    return {
        "place": f'{loc["name"]}, {loc.get("country", "")}',
        "current": w["current"], "daily": days,
        "source": "Open Meteo", "forecast_scope": "current and next 5 days",
    }
