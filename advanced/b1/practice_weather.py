"""
Урок B1 — ПРАКТИЧЕСКАЯ РАБОТА 1 (Блок 1: функции вглубь)

Мини-пайплайн получения погоды через Open-Meteo (JSON API, без ключа):

    fetch_weather()   -> raw: dict        # сырой JSON-ответ (дано)
    extract_fields()  -> fields: dict     # TODO: нужные ключи/значения в ПЛОСКИЙ словарь
    build_message()   -> text: str        # TODO: сообщение из **kwargs (без отправки!)
    WeatherData(**fields)                 # тот же словарь распаковываем в ОБЪЕКТ модели

Здесь сходятся все темы блока:
  - **kwargs: build_message(**fields) и WeatherData(**fields) — распаковка словаря;
  - словарь как набор "ключ -> значение";
  - WMO_DESCRIPTIONS — словарь-справочник кодов погоды;
  - WeatherData — объект, который "уже живёт", хотя БД ещё нет.

Запуск:  python practice_weather.py
Сеть не обязательна: по умолчанию демо использует вшитый SAMPLE_RESPONSE.
Зависимости:  pip install -r requirements.txt
Решение:  solutions/practice_weather_solution.py
"""

import requests


# --- Реальный ответ Open-Meteo (Москва) — чтобы работать офлайн и детерминированно ---
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


# --- Справочник кодов погоды WMO -> человеческое описание (дано) ---
WMO_DESCRIPTIONS = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Изморозь",
    51: "Слабая морось",
    53: "Морось",
    55: "Сильная морось",
    61: "Небольшой дождь",
    63: "Дождь",
    65: "Сильный дождь",
    71: "Небольшой снег",
    73: "Снег",
    75: "Сильный снег",
    80: "Кратковременный дождь",
    95: "Гроза",
}


# --- Модель данных (дано). Имена параметров СПЕЦИАЛЬНО совпадают с ключами ---
# --- плоского словаря, поэтому объект создаётся одной распаковкой: WeatherData(**fields). ---
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

    # Когда появится БД — здесь будет вставка строки. Пока объект просто живёт в памяти.
    # def save(self, db): ...


def fetch_weather(latitude: float, longitude: float) -> dict:
    """Тянет текущую погоду с Open-Meteo и возвращает сырой JSON как dict.
    При проблемах с сетью возвращает вшитый SAMPLE_RESPONSE — чтобы демо не падало."""
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


# === TODO 1. extract_fields ===
# Достань из сырого ответа нужные данные и собери их в ОДИН ПЛОСКИЙ словарь.
# Это и есть "сбор всех ключей и значений в одном месте".
#
# Вход:  raw  — dict как SAMPLE_RESPONSE
#        city — название города (в ответе его нет, передаём руками)
# Выход: словарь РОВНО с такими ключами (совпадают с параметрами WeatherData!):
#   city, time, temperature, feels_like, humidity,
#   wind_speed, wind_direction, pressure, description
#
# Где что лежит (всё внутри raw["current"]):
#   temperature     <- current["temperature_2m"]
#   feels_like      <- current["apparent_temperature"]
#   humidity        <- current["relative_humidity_2m"]
#   wind_speed      <- current["wind_speed_10m"]
#   wind_direction  <- current["wind_direction_10m"]
#   pressure        <- current["surface_pressure"]
#   time            <- current["time"]
#   description     <- WMO_DESCRIPTIONS по ключу current["weather_code"]
#                      (если кода нет в справочнике — верни "неизвестно")
#
# def extract_fields(raw: dict, city: str) -> dict:
#     ...


# === TODO 2. build_message ===
# Собери из ИМЕНОВАННЫХ аргументов читаемое сообщение (НЕ отправляем — просто строка).
# Подпись с **kwargs: все ключи прилетят в fields как словарь.
# Пройди по fields.items() и собери строки вида "ключ: значение".
#
# Пример вызова:  build_message(**extract_fields(raw, "Москва"))
#
# def build_message(**fields) -> str:
#     ...


def demo_weather():
    print("== Практика 1: погода через Open-Meteo ==")

    # 1) Получаем сырой JSON (по умолчанию — офлайн-образец).
    raw = SAMPLE_RESPONSE
    # raw = fetch_weather(55.75, 37.62)   # раскомментируй для реального запроса

    # 2) Собираем плоский словарь "ключ -> значение".
    # fields = extract_fields(raw, city="Москва")
    # print(fields)

    # 3) Формируем сообщение из **kwargs (распаковка словаря в именованные аргументы).
    # print(build_message(**fields))

    # 4) Тот же словарь распаковываем в объект модели — он "живёт" до появления БД.
    # weather = WeatherData(**fields)
    # print(repr(weather))


if __name__ == "__main__":
    demo_weather()
