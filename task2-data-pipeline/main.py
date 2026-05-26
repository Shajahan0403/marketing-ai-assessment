import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

URL = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 13.0827,
    "longitude": 80.2707,
    "hourly": "temperature_2m"
}

try:
    logging.info("Fetching weather data...")

    response = requests.get(URL, params=params)
    response.raise_for_status()

    data = response.json()

    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

    df = pd.DataFrame({
        "time": times,
        "temperature": temps
    })

    # Derived field
    df["temperature_fahrenheit"] = (df["temperature"] * 9/5) + 32

    df.to_csv("sample_output.csv", index=False)

    logging.info("Data saved successfully!")

except Exception as e:
    logging.error(f"Error: {e}")