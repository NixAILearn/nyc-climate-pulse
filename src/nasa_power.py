import pandas as pd
import requests

URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
PARAMETERS = "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M"


def fetch_daily(start, end, latitude=40.71, longitude=-74.01):
    """Download daily NASA POWER weather data and return it as a DataFrame."""
    params = {
        "parameters": PARAMETERS,
        "community": "RE",
        "latitude": latitude,
        "longitude": longitude,
        "start": start,
        "end": end,
        "format": "JSON",
    }
    response = requests.get(URL, params=params, timeout=120)
    response.raise_for_status()

    data = response.json()["properties"]["parameter"]
    df = pd.DataFrame(data)
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    df.index.name = "date"
    return df.replace(-999, float("nan"))