"""Weather service module.

A module to fetch weather data from OpenWeatherMap API.

Author:
    Paulo Sanchez (@erlete)
"""


import os
from time import time
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise ValueError(
        "No API key found. Set the OPENWEATHER_API_KEY environment variable."
    )


class WheaterService:
    """Weather service class.

    A class to fetch and store weather data from OpenWeatherMap API.

    Attributes:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        revalidation_period (int): Revalidation period of the data in seconds.
        BASE_URL (str): Base URL of the OpenWeatherMap API.

    Properties:
        data (Any): Get weather data.
        clouds_data (Any): Get cloud data.
        clouds_all (float): Get cloudiness in percentage.
        humidity (float): Get humidity in percentage.
        name (str): Get name of the location.
        pressure_ground_level (float): Get pressure at ground level in hPa.
        pressure_sea_level (float): Get pressure at sea level in hPa.
        temperature_data (Any): Get temperature data.
        temperature (float): Get temperature in Celsius.
        temperature_max (float): Get maximum temperature in Celsius.
        temperature_min (float): Get minimum temperature in Celsius.
        visibility (float): Get visibility in meters (up to 10.000).
        wind_data (Any): Get wind data.
        wind_orientation (float): Get wind orientation in degrees.
        wind_gust (float): Get wind gust in m/s.
        wind_speed (float): Get wind speed in m/s.
    """

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    def __init__(
        self,
        latitude: float,
        longitude: float,
        revalidation_period: int = 60
    ) -> None:
        """Initialize Weather object.

        Args:
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.
            revalidation_period (int): Revalidation period of the data in
                seconds.
        """
        self.latitude = latitude
        self.longitude = longitude
        self.revalidation_period = revalidation_period

        # Internal attributes and first data fetch:
        self._timestamp = 0.0
        self._data = self._fetch_weather_data()

    @property
    def data(self) -> Any:
        """Get weather data."""
        return self._fetch_weather_data()

    @property
    def clouds_data(self) -> dict[str, int | float]:
        """Get cloud data."""
        return self.data["clouds"]

    @property
    def clouds_all(self) -> int | float:
        """Get cloudiness in percentage."""
        return self.data["clouds"]["all"]

    @property
    def humidity(self) -> int | float:
        """Get humidity in percentage."""
        return self.data["main"]["humidity"]

    @property
    def name(self) -> str:
        """Get name of the location."""
        return self.data["name"]

    @property
    def pressure_ground_level(self) -> int | float:
        """Get pressure at ground level in hPa."""
        return self.data["main"]["grnd_level"]

    @property
    def pressure_sea_level(self) -> int | float:
        """Get pressure at sea level in hPa."""
        return self.data["main"]["sea_level"]

    @property
    def temperature_data(self) -> dict[str, int | float]:
        """Get temperature data."""
        return {
            "temp": self.data["main"]["temp"],
            "temp_min": self.data["main"]["temp_min"],
            "temp_max": self.data["main"]["temp_max"]
        }

    @property
    def temperature(self) -> int | float:
        """Get temperature in Celsius."""
        return self.data["main"]["temp"]

    @property
    def temperature_max(self) -> int | float:
        """Get maximum temperature in Celsius."""
        return self.data["main"]["temp_max"]

    @property
    def temperature_min(self) -> int | float:
        """Get minimum temperature in Celsius."""
        return self.data["main"]["temp_min"]

    @property
    def visibility(self) -> int | float:
        """Get visibility in meters (up to 10.000)."""
        return self.data["visibility"]

    @property
    def wind_data(self) -> dict[str, int | float]:
        """Get wind data."""
        return self.data["wind"]

    @property
    def wind_orientation(self) -> int | float:
        """Get wind orientation in degrees."""
        return self.data["wind"]["deg"]

    @property
    def wind_gust(self) -> int | float:
        """Get wind gust in m/s."""
        return self.data["wind"]["gust"]

    @property
    def wind_speed(self) -> int | float:
        """Get wind speed in m/s."""
        return self.data["wind"]["speed"]

    def _fetch_weather_data(self) -> dict[str, Any]:
        if time() - self._timestamp > self.revalidation_period:
            response = requests.get(
                f"{self.BASE_URL}?"
                + "&".join((
                    f"lat={self.latitude}&&&",
                    f"lon={self.longitude}",
                    "units=metric",
                    f"appid={API_KEY}"
                )),
                timeout=5
            )
            data = response.json()

            if response.status_code == 200:
                self._timestamp = time()
                self._data = data
            else:
                raise ValueError(f"Error while fetching wheater data: {data}")

        return self._data


if __name__ == "__main__":
    weather = WheaterService(42.341362, -7.862555)

    for _ in range(10):
        weather_data = weather.data

    print(f"Temperature: {weather.temperature}°C")
    print(f"Humidity: {weather.humidity}%")
    print(f"Wind Speed: {weather.wind_speed} m/s")
    print(f"Cloudiness: {weather.clouds_all}%")
    print(f"Visibility: {weather.visibility} meters")
    print(f"Pressure (Ground Level): {weather.pressure_ground_level} hPa")
    print(f"Pressure (Sea Level): {weather.pressure_sea_level} hPa")
    print(f"Location Name: {weather.name}")
    print("-" * 40)
