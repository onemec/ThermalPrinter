from typing import Annotated

import requests
from datetime import datetime
from pydantic import BaseModel, ValidationError, Field
from dominate.tags import br, i, p, div, link
from dominate.util import text


class DailyWeather(BaseModel):
    """
    Model representing daily weather data.

    Attributes
    ----------
    time : list[datetime]
        List of datetime objects representing the time of each weather data point.
    weathercode : list[Annotated[int, Field(ge=0, le=99)]]
        List of weather codes, constrained to be between 0 and 99.
    temperature_2m_max : list[float]
        List of maximum temperatures at 2 meters above ground level.
    temperature_2m_min : list[float]
        List of minimum temperatures at 2 meters above ground level.
    sunrise : list[float]
        List of sunrise times.
    sunset : list[float]
        List of sunset times.
    precipitation_sum : list[float]
        List of total precipitation amounts.
    """

    time: list[datetime]
    weathercode: list[Annotated[int, Field(ge=0, le=99)]]
    temperature_2m_max: list[float]
    temperature_2m_min: list[float]
    sunrise: list[float]
    sunset: list[float]
    precipitation_sum: list[float]


class CurrentWeather(BaseModel):
    """
    Model representing current weather data.

    Attributes
    ----------
    temperature : float
        Current temperature.
    windspeed : float
        Current wind speed.
    winddirection : float
        Current wind direction.
    weathercode : Annotated[int, Field(ge=0, le=99)]
        Current weather code, constrained to be between 0 and 99.
    is_day : int
        Indicator if it is day (1) or night (0).
    time : datetime
        Current time.
    """

    temperature: float
    windspeed: float
    winddirection: float
    weathercode: Annotated[int, Field(ge=0, le=99)]
    is_day: int
    time: datetime


class WeatherResponse(BaseModel):
    """
    Model representing the weather response containing current and daily weather data.

    Attributes
    ----------
    current_weather : CurrentWeather
        Instance of CurrentWeather containing current weather data.
    daily : DailyWeather
        Instance of DailyWeather containing daily weather data.
    """

    current_weather: CurrentWeather
    daily: DailyWeather


def wmo_to_fa(wmo_code: int) -> str:
    """
    Convert a given WMO weather code to the corresponding Font Awesome tag.

    Parameters
    ----------
    wmo_code : int
        The WMO weather code to be converted.

    Returns
    -------
    str
        The Font Awesome tag representing the WMO weather code.
    """
    return {
        0: "fa-sun",  # Cloud development not observed or not observable
        1: "fa-cloud-sun",  # Clouds generally dissolving or becoming less developed
        2: "fa-cloud",  # State of sky on the whole unchanged
        3: "fa-cloud-moon",  # Clouds generally forming or developing
        4: "fa-cloud-showers-heavy",
        # Cumulonimbus or cumulus congestus, with little vertical extent, little or no precipitation
        5: "fa-cloud-showers-heavy",
        # Cumulonimbus or cumulus congestus, with moderate or heavy vertical extent, usually with heavy precipitation
        6: "fa-cloud-rain",
        # Cumulonimbus or cumulus congestus, with towering vertical development, usually with heavy precipitation
        7: "fa-cloud-showers-heavy",  # Moderate or heavy cumulonimbus or cumulus congestus with frequent lightning
        8: "fa-cloud-showers-heavy",
        # Cumulonimbus with very heavy vertical development, usually with extreme precipitation
        9: "fa-cloud-hail",
        # Cumulonimbus with tops in the form of an anvil and often with cirrus or cirrostratus above
        10: "fa-cloud-meatball",  # Towering cumulus or cumulus fractus in an otherwise clear sky
        11: "fa-bolt",  # Precipitation within sight, not reaching the ground or the surface of the sea
        12: "fa-bolt",
        # Precipitation within sight, reaching the ground or the surface of the sea, but distant, i.e. not over the
        # station
        13: "fa-bolt",
        # Precipitation within sight, reaching the ground or the surface of the sea, near to the station, but not at
        # the station
        14: "fa-bolt",
        # Precipitation within sight, reaching the ground or the surface of the sea at the station, but not directly
        # at the station
        15: "fa-bolt",
        # Precipitation within sight, reaching the ground or the surface of the sea at the station, and being blown
        # by the wind
        16: "fa-snowflake",  # Precipitation within sight, but not at the station
        17: "fa-snowflake",  # Ice pellets or snow grains within sight, but not at the station
        18: "fa-cloud-rain",
        # Precipitation within sight, reaching the ground or the surface of the sea at the station, but not directly
        # at the station
        19: "fa-cloud-rain",  # Precipitation within sight, and being blown by the wind
        20: "fa-fog",
        # Fog or ice fog at the station, the fog or ice fog being the same as or thinner than the smallest
        # subdivision of the time period during which it is reported
        21: "fa-fog",
        # Fog or ice fog at the station, the fog or ice fog being denser than the smallest subdivision of the time
        # period during which it is reported, but not dense enough to meet the criteria for the subsequent code
        22: "fa-fog",
        # Fog or ice fog at the station, the fog or ice fog being denser than the smallest subdivision of the time
        # period during which it is reported and becoming denser or the horizontal visibility decreasing during the
        # past hour
        23: "fa-fog",
        # Fog or ice fog at the station, the fog or ice fog being denser than the smallest subdivision of the time
        # period during which it is reported and becoming less dense or the horizontal visibility increasing during
        # the past hour
        24: "fa-wind",
        # Fog or ice fog, in the form of a layer or patch, at the station, whether on land or sea, the fog or ice fog
        # extending to a level above that of the observer
        25: "fa-wind",
        # Fog or ice fog, in the form of a layer or patch, not at the station, whether on land or sea, the fog or ice
        # fog extending to a level above that of the observer
        26: "fa-smog",
        # Fog or ice fog at the station, the fog or ice fog being the same as or thinner than the smallest
        # subdivision of the time period during which it is reported
        27: "fa-smog",
        # Fog or ice fog at the station, the fog or ice fog being denser than the smallest subdivision of the time
        # period during which it is reported, but not dense enough to meet the criteria for the subsequent code
        28: "fa-smog",
        # Fog or ice fog at the station, the fog or ice fog being denser than the smallest subdivision of the time
        # period during which it is reported and becoming denser or the horizontal visibility decreasing during the
        # past hour
        29: "fa-smog",
        # Fog or ice fog at the station, the fog or ice fog being denser than the smallest subdivision of the time
        # period during which it is reported and becoming less dense or the horizontal visibility increasing during
        # the past hour
        30: "fa-smog",
        # Fog or ice fog, in the form of a layer or patch, at the station, whether on land or sea, the fog or ice fog
        # extending to a level above that of the observer
        31: "fa-smog",
        # Fog or ice fog, in the form of a layer or patch, not at the station, whether on land or sea, the fog or ice
        # fog extending to a level above that of the observer
        32: "fa-clouds",  # Widespread dust in suspension in the air at the station, whether over land or sea
        33: "fa-dust",  # Widespread sand in suspension in the air at the station, whether over land or sea
        34: "fa-wind",  # Widespread dust or sand in suspension in the air at the station, whether over land or sea
        35: "fa-dust",
        # Widespread dust raised by the wind at or near the station at the time of observation, but no duststorm or
        # sandstorm within sight at that time
        36: "fa-wind",
        # Widespread sand raised by the wind at or near the station at the time of observation, but no duststorm or
        # sandstorm within sight at that time
        37: "fa-smog",
        # Widespread dust or sand raised by the wind at or near the station at the time of observation,
        # but no duststorm or sandstorm within sight at that time
        38: "fa-cloud-sun",  # Widespread dust in suspension in the air at the station, whether over land or sea
        39: "fa-dust",  # Widespread sand in suspension in the air at the station, whether over land or sea
        40: "fa-wind",  # Widespread dust or sand in suspension in the air at the station, whether over land or sea
        41: "fa-dust",
        # Widespread dust raised by the wind at or near the station at the time of observation, but no duststorm or
        # sandstorm within sight at that time
        42: "fa-wind",
        # Widespread sand raised by the wind at or near the station at the time of observation, but no duststorm or
        # sandstorm within sight at that time
        43: "fa-smog",
        # Widespread dust or sand raised by the wind at or near the station at the time of observation,
        # but no duststorm or sandstorm within sight at that time
        44: "fa-cloud",  # Fogs or ice fog at the station, the fog or ice fog ending during the period of observation
        45: "fa-clouds",
        # Fogs or ice fog at the station, the fog or ice fog, which was the same as or thinner than the smallest
        # subdivision of the time period during which it is reported, ending during the period of observation
        46: "fa-smog",
        # Fogs or ice fog at the station, the fog or ice fog, which was denser than the smallest subdivision of the
        # time period during which it is reported, ending during the period of observation
        47: "fa-wind",
        # Fogs or ice fog at the station, the fog or ice fog, which was denser than the smallest subdivision of the
        # time period during which it is reported and becoming less dense or the horizontal visibility increasing
        # during the past hour, ending during the period of observation
        48: "fa-wind",
        # Fogs or ice fog, in the form of a layer or patch, at the station, whether on land or sea, the fog or ice
        # fog ending during the period of observation
        49: "fa-smog",
        # Fogs or ice fog, in the form of a layer or patch, at the station, whether on land or sea, the fog or ice
        # fog, which was denser than the smallest subdivision of the time period during which it is reported,
        # ending during the period of observation
        50: "fa-sun",
        # Drizzle at the station during the preceding hour or at the time of observation, but not at the time of
        # observation
        51: "fa-cloud-showers",  # Drizzle at the station, which did not start or stop during the preceding hour
        52: "fa-cloud-showers-heavy",  # Drizzle at the station, which started or stopped during the preceding hour
        53: "fa-cloud-rain",
        # Rain at the station during the preceding hour or at the time of observation, but not at the time of
        # observation
        54: "fa-cloud-rain",  # Rain at the station, which did not start or stop during the preceding hour
        55: "fa-cloud-rain",  # Rain at the station, which started or stopped during the preceding hour
        56: "fa-cloud-showers-heavy",
        # Precipitation consisting of rain alone or in combination with snow pellets, snow grains, or ice pellets at
        # the station during the preceding hour or at the time of observation, but not at the time of observation
        57: "fa-cloud-showers-heavy",
        # Precipitation consisting of rain alone or in combination with snow pellets, snow grains, or ice pellets at
        # the station, which did not start or stop during the preceding hour
        58: "fa-cloud-showers-heavy",
        # Precipitation consisting of rain alone or in combination with snow pellets, snow grains, or ice pellets at
        # the station, which started or stopped during the preceding hour
        59: "fa-cloud-snow",
        # Precipitation consisting solely of snow, or of rain and snow, at the station during the preceding hour or
        # at the time of observation, but not at the time of observation
        60: "fa-cloud-snow",
        # Precipitation consisting solely of snow, or of rain and snow, at the station, which did not start or stop
        # during the preceding hour
        61: "fa-cloud-snow",
        # Precipitation consisting solely of snow, or of rain and snow, at the station, which started or stopped
        # during the preceding hour
        62: "fa-cloud-snow",
        # Intermittent slight snow, with or without rain, at the station during the preceding hour or at the time of
        # observation, but not at the time of observation
        63: "fa-cloud-snow",
        # Intermittent slight snow, with or without rain, at the station, which did not start or stop during the
        # preceding hour
        64: "fa-cloud-snow",
        # Intermittent slight snow, with or without rain, at the station, which started or stopped during the
        # preceding hour
        65: "fa-cloud-snow",
        # Continuous slight snowfall at the station during the preceding hour or at the time of observation,
        # but not at the time of observation
        66: "fa-cloud-snow",
        # Continuous slight snowfall at the station, which did not start or stop during the preceding hour
        67: "fa-cloud-snow",
        # Continuous slight snowfall at the station, which started or stopped during the preceding hour
        68: "fa-cloud-snow",
        # Intermittent moderate snow, with or without rain, at the station during the preceding hour or at the time
        # of observation, but not at the time of observation
        69: "fa-cloud-snow",
        # Intermittent moderate snow, with or without rain, at the station, which did not start or stop during the
        # preceding hour
        70: "fa-cloud-snow",
        # Intermittent moderate snow, with or without rain, at the station, which started or stopped during the
        # preceding hour
        71: "fa-cloud-snow",
        # Continuous moderate snowfall at the station during the preceding hour or at the time of observation,
        # but not at the time of observation
        72: "fa-cloud-snow",
        # Continuous moderate snowfall at the station, which did not start or stop during the preceding hour
        73: "fa-cloud-snow",
        # Continuous moderate snowfall at the station, which started or stopped during the preceding hour
        74: "fa-cloud-snow",
        # Intermittent heavy snow, with or without rain, at the station during the preceding hour or at the time of
        # observation, but not at the time of observation
        75: "fa-cloud-snow",
        # Intermittent heavy snow, with or without rain, at the station, which did not start or stop during the
        # preceding hour
        76: "fa-cloud-snow",
        # Intermittent heavy snow, with or without rain, at the station, which started or stopped during the
        # preceding hour
        77: "fa-cloud-snow",
        # Continuous heavy snowfall at the station during the preceding hour or at the time of observation,
        # but not at the time of observation
        78: "fa-cloud-snow",
        # Continuous heavy snowfall at the station, which did not start or stop during the preceding hour
        79: "fa-cloud-snow",
        # Continuous heavy snowfall at the station, which started or stopped during the preceding hour
        80: "fa-cloud-showers",
        # Drizzle or rain and snow at the station during the preceding hour or at the time of observation, but not at
        # the time of observation
        81: "fa-cloud-showers",
        # Drizzle or rain and snow at the station, which did not start or stop during the preceding hour
        82: "fa-cloud-showers",
        # Drizzle or rain and snow at the station, which started or stopped during the preceding hour
        83: "fa-cloud-showers-heavy",
        # Rain and snow at the station during the preceding hour or at the time of observation, but not at the time
        # of observation
        84: "fa-cloud-showers-heavy",
        # Rain and snow at the station, which did not start or stop during the preceding hour
        85: "fa-cloud-showers-heavy",
        # Rain and snow at the station, which started or stopped during the preceding hour
        86: "fa-cloud-snow",
        # Light showers of ice pellets at the station during the preceding hour or at the time of observation,
        # but not at the time of observation
        87: "fa-cloud-snow",
        # Light showers of ice pellets at the station, which did not start or stop during the preceding hour
        88: "fa-cloud-snow",
        # Light showers of ice pellets at the station, which started or stopped during the preceding hour
        89: "fa-cloud-snow",
        # Moderate or heavy showers of ice pellets at the station during the preceding hour or at the time of
        # observation, but not at the time of observation
        90: "fa-cloud-snow",
        # Moderate or heavy showers of ice pellets at the station, which did not start or stop during the preceding hour
        91: "fa-cloud-snow",
        # Moderate or heavy showers of ice pellets at the station, which started or stopped during the preceding hour
        92: "fa-cloud-snow",
        # Slight or moderate snow pellets at the station during the preceding hour or at the time of observation,
        # but not at the time of observation
        93: "fa-cloud-snow",
        # Slight or moderate snow pellets at the station, which did not start or stop during the preceding hour
        94: "fa-cloud-snow",
        # Slight or moderate snow pellets at the station, which started or stopped during the preceding hour
        95: "fa-cloud-snow",
        # Slight or moderate hail at the station during the preceding hour or at the time of observation, but not at
        # the time of observation
        96: "fa-cloud-snow",
        # Slight or moderate hail at the station, which did not start or stop during the preceding hour
        97: "fa-cloud-snow",
        # Slight or moderate hail at the station, which started or stopped during the preceding hour
        98: "fa-cloud-showers-heavy",
        # Light showers of snow at the station during the preceding hour or at the time of observation, but not at
        # the time of observation
        99: "fa-cloud-showers-heavy",
        # Light showers of snow at the station, which did not start or stop during the preceding hour
    }.get(wmo_code)


def get_weather():
    """
    Fetch the current weather and daily forecast data from the Open-Meteo API.

    This function sends a GET request to the Open-Meteo API to retrieve weather data
    for a specific location (latitude: 40.75, longitude: -73.94). The data includes
    current weather conditions and daily forecasts such as weather code, maximum and
    minimum temperatures, sunrise and sunset times, and precipitation.

    Returns
    -------
    WeatherResponse
        An instance of the WeatherResponse class containing the parsed weather data.

    Raises
    ------
    ConnectionError
        If the API response status code is not 200 (OK).
    ValidationError
        If the JSON response cannot be validated against the WeatherResponse model.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast?latitude=40.75&longitude=-73.94"
        "&daily=weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum"
        "&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph"
        "&precipitation_unit=inch&timeformat=unixtime&timezone=America%2FNew_York"
    )
    r = requests.get(url)
    if r.status_code != 200:
        raise ConnectionError(
            f"Got {r.status_code} response (instead of 200) while fetching weather"
        )
    try:
        return WeatherResponse(**r.json())
    except ValidationError as e:
        raise ValidationError(e.errors())


def generate() -> div:
    """
    Generate an HTML div element containing the weather forecast.

    This function fetches the current weather and daily forecast data,
    then constructs an HTML div element with the weather information
    formatted for display.

    Returns
    -------
    div
        An HTML div element with the weather forecast.
    """
    wr = get_weather()
    formed_div = div(cls="row mb-3 text-center forecast")
    with formed_div:
        link()
        with div(cls="col"):
            br()
            i(cls=f"fa-solid {wmo_to_fa(wr.current_weather.weathercode)} fa-4x")
        with div(cls="col"):
            with div(cls="row"):
                text(
                    f"<h5>{wr.current_weather.temperature:.1f}&degF</h5>", escape=False
                )
            with div(cls="row"):
                with p():
                    i(cls="fa-solid fa-wind fa-sm")
                    text(f" {wr.current_weather.windspeed:.1f} mph ")
                    br()
                    i(cls="fa-solid fa-arrow-up-long")
                    text(f" {wr.daily.temperature_2m_max[0]}&degF ", escape=False)
                    i(cls="fa-solid fa-arrow-down-long")
                    text(f" {wr.daily.temperature_2m_min[0]}&degF ", escape=False)
                    br()
                    i(cls="fa-regular fa-sun")
                    text(
                        f" {datetime.fromtimestamp(wr.daily.sunrise[0]).strftime('%H:%M')} "
                    )
                    i(cls="fa-solid fa-arrow-right-long")
                    text(
                        f" {datetime.fromtimestamp(wr.daily.sunset[0]).strftime('%H:%M')} "
                    )
    return formed_div
