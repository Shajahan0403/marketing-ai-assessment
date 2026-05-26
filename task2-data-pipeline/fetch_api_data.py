import requests
import pandas as pd
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class APIDataFetcher:
    """Fetch and process data from various APIs"""
    
    def __init__(self, output_dir="./"):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'MarketingAI-DataPipeline/1.0'})
    
    def fetch_weather_data(self, latitude, longitude, output_file="weather_data.csv"):
        """Fetch weather data from Open-Meteo API"""
        try:
            logging.info(f"Fetching weather data for coordinates ({latitude}, {longitude})...")
            
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "hourly": "temperature_2m,relative_humidity_2m,precipitation",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "auto"
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Process hourly data
            hourly_data = pd.DataFrame({
                "time": data["hourly"]["time"],
                "temperature_celsius": data["hourly"]["temperature_2m"],
                "humidity_percent": data["hourly"]["relative_humidity_2m"],
                "precipitation_mm": data["hourly"]["precipitation"]
            })
            
            # Convert temperature to Fahrenheit
            hourly_data["temperature_fahrenheit"] = (hourly_data["temperature_celsius"] * 9/5) + 32
            
            # Save to CSV
            output_path = f"{self.output_dir}/{output_file}"
            hourly_data.to_csv(output_path, index=False)
            
            logging.info(f"Weather data saved to {output_path} ({len(hourly_data)} records)")
            return hourly_data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            raise
        except Exception as e:
            logging.error(f"Error processing weather data: {e}")
            raise
    
    def fetch_json_api(self, url, output_file="api_data.json", params=None):
        """Fetch data from a generic JSON API"""
        try:
            logging.info(f"Fetching data from {url}...")
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Save to JSON
            output_path = f"{self.output_dir}/{output_file}"
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logging.info(f"Data saved to {output_path}")
            return data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            raise
        except Exception as e:
            logging.error(f"Error processing API data: {e}")
            raise
    
    def fetch_multiple_apis(self, api_list):
        """Fetch data from multiple APIs"""
        results = {}
        for api_config in api_list:
            try:
                url = api_config.get("url")
                output_file = api_config.get("output_file", "data.json")
                api_type = api_config.get("type", "json")
                
                if api_type == "weather":
                    lat = api_config.get("latitude")
                    lon = api_config.get("longitude")
                    results[output_file] = self.fetch_weather_data(lat, lon, output_file)
                else:
                    results[output_file] = self.fetch_json_api(url, output_file)
                    
            except Exception as e:
                logging.warning(f"Failed to fetch from {api_config}: {e}")
                continue
        
        return results


if __name__ == "__main__":
    # Example usage
    fetcher = APIDataFetcher(output_dir="./")
    
    # Fetch weather data for Chennai, India
    weather_df = fetcher.fetch_weather_data(
        latitude=13.0827,
        longitude=80.2707,
        output_file="api_weather_data.csv"
    )
    
    print("\nWeather Data Summary:")
    print(f"Records: {len(weather_df)}")
    print(f"Temperature Range: {weather_df['temperature_celsius'].min():.1f}°C to {weather_df['temperature_celsius'].max():.1f}°C")
    print(f"\nFirst 5 records:\n{weather_df.head()}")
