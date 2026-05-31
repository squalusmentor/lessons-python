"""
Урок B1 — РЕШЕНИЕ практической работы 1 (погода через Open-Meteo).

Самодостаточный файл: запускается напрямую (python solutions/practice_weather_solution.py).
По умолчанию использует офлайн-образец SAMPLE_RESPONSE; для реального запроса
раскомментируй вызов fetch_weather() в demo_weather().
"""

import requests


SAMPLE_RESPONSE = {
    "latitude": 55.75,
    "longitude": 37.625,
    "timezone": "Europe/Moscow",
    "elevation": 152.0,
    "current_units": {
        "temperature_2m": "°C",
        "relative_humidity_2m": "%",
        "apparent_temperature": "°C",
        "wind_speed_10m": "km/h",
        "wind_direction_10m": "°",
        "weather_code": "wmo code",
        "surface_pressure": "hPa",
    },
    "current": {
        "time": "2026-05-31T12:45",
        "temperature_2m": 15.5,
        "relative_humidity_2m": 58,
        "apparent_temperature": 14.0,
        "wind_speed_10m": 6.4,
        "wind_direction_10m": 63,
        "weather_code": 3,
        "surface_pressure": 991.6,
    },
}

WMO_DESCRIPTIONS = {
    0: "Ясно", 1: "Преимущественно ясно", 2: "Переменная облачность", 3: "Пасмурно",
    45: "Туман", 48: "Изморозь",
    51: "Слабая морось", 53: "Морось", 55: "Сильная морось",
    61: "Небольшой дождь", 63: "Дождь", 65: "Сильный дождь",
    71: "Небольшой снег", 73: "Снег", 75: "Сильный снег",
    80: "Кратковременный дождь", 95: "Гроза",
}


class WeatherData:
    def __init__(self, city, time, temperature, feels_like, humidity,
                 wind_speed, wind_direction, pressure, description):
        self.city = city
        self.time = time
        self.temperature = temperature
        self.feels_like = feels_like
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.pressure = pressure
        self.description = description

    def __repr__(self) -> str:
        return (f"WeatherData(city={self.city!r}, temperature={self.temperature}, "
                f"description={self.description!r})")


def fetch_weather(latitude: float, longitude: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": "Europe/Moscow",
        "current": ("temperature_2m,relative_humidity_2m,apparent_temperature,"
                    "wind_speed_10m,wind_direction_10m,weather_code,surface_pressure"),
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"  [сеть недоступна: {e}; беру SAMPLE_RESPONSE]")
        return SAMPLE_RESPONSE


# --- РЕШЕНИЕ TODO 1 ---
def extract_fields(raw: dict, city: str) -> dict:
    current = raw["current"]
    code = current["weather_code"]
    return {
        "city": city,
        "time": current["time"],
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "wind_direction": current["wind_direction_10m"],
        "pressure": current["surface_pressure"],
        "description": WMO_DESCRIPTIONS.get(code, "неизвестно"),
    }


# --- РЕШЕНИЕ TODO 2 ---
def build_message(**fields) -> str:
    title = f"Погода: {fields.get('city', '—')}"
    lines = [title, "-" * len(title)]
    for key, value in fields.items():
        lines.append(f"{key}: {value}")
    return "\n".join(lines)


def demo_weather():
    print("== Решение практики 1: погода через Open-Meteo ==")

    raw = SAMPLE_RESPONSE
    # raw = fetch_weather(55.75, 37.62)   # реальный запрос

    # Собрали плоский словарь "ключ -> значение".
    fields = extract_fields(raw, city="Москва")

    # Распаковали словарь в **kwargs — получили сообщение.
    print(build_message(**fields))
    print()

    # Тот же словарь распаковали в объект модели.
    weather = WeatherData(**fields)
    print(repr(weather))
    print("  weather.feels_like =", weather.feels_like)


if __name__ == "__main__":
    demo_weather()
