"""Utilities module.

Author:
    Paulo Sanchez (@erlete)
"""


import math

COVER_RADIUS = 133.97459621556135  # [m]


def geo_distance_to_m(lat1, lon1, lat2, lon2) -> float:
    """Measure the distance between two points in meters.

    Args:
        lat1 (float): Latitude of the first point.
        lon1 (float): Longitude of the first point.
        lat2 (float): Latitude of the second point.
        lon2 (float): Longitude of the second point.

    Returns:
        float: Distance between the two points in meters.

    Reference:
        https://en.wikipedia.org/wiki/Haversine_formula
    """
    earth_radius = 6378.137  # Radius of earth in KM
    d_lat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    d_lon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = (
        math.sin(d_lat/2) * math.sin(d_lat/2)
        + math.cos(lat1 * math.pi / 180)
        * math.cos(lat2 * math.pi / 180)
        * math.sin(d_lon/2) * math.sin(d_lon/2)
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = earth_radius * c
    return d * 1000  # [m]


def radius_to_lat_lon_units(lat, lon, radius) -> tuple[float, float]:
    """Convert a radius in meters to latitude and longitude units.

    Args:
        lat (float): Latitude of the center point.
        lon (float): Longitude of the center point.
        radius (float): Radius in meters.

    Returns:
        tuple: Radius in latitude and longitude units.
    """
    earth_radius = 6378.137  # Radius of earth in KM
    radius_km = radius / 1000  # Convert radius to kilometers

    # Calculate the change in latitude
    delta_lat = (radius_km / earth_radius) * (180 / math.pi)

    # Calculate the change in longitude
    delta_lon = (radius_km / (earth_radius *
                 math.cos(math.pi * lat / 180))) * (180 / math.pi)

    return delta_lat, delta_lon


predefined_route = {
    "x": [
        0.0020161290322580627,
        0.1754032258064516,
        0.30645161290322576,
        0.4032258064516129,
        0.497983870967742,
        0.5362903225806451,
        0.3306451612903226,
        0.04032258064516128,
        0.10887096774193547,
        0.33669354838709675,
        0.5,
        0.6935483870967742,
        0.8205645161290323,
        0.9919354838709676
    ],
    "y": [
        0.005952380952380959,
        0.18722943722943727,
        0.308982683982684,
        0.400974025974026,
        0.4902597402597403,
        0.7418831168831169,
        0.9880952380952382,
        0.833874458874459,
        0.5064935064935066,
        0.42261904761904767,
        0.49837662337662336,
        0.6931818181818182,
        0.833874458874459,
        0.9935064935064936
    ]
}
