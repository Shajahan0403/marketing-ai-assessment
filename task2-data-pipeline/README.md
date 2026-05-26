# Weather Data Pipeline

## Project Overview

This project demonstrates a simple data pipeline using a public API, Python, and BigQuery.

The pipeline fetches weather data from the Open-Meteo API, transforms the data, and stores it in Google BigQuery.

---

## API Used

Open-Meteo API

Website:
https://open-meteo.com/

---

## Why I Chose This API

I selected Open-Meteo because:
- It is free to use
- No API key is required
- It provides structured weather data
- It is beginner-friendly

---

## Technologies Used

- Python
- Pandas
- Requests
- Google BigQuery
- VS Code
- GitHub

---

## How to Run the Pipeline

### Step 1

Install dependencies:

pip install requests pandas

### Step 2

Run the Python script:

python main.py

### Step 3

The script generates:

sample_output.csv

---

## Data Transformation

The pipeline performs:
- Data cleaning
- Tabular formatting
- Temperature conversion from Celsius to Fahrenheit

Derived field:
temperature_fahrenheit

---

## BigQuery Setup

### Project Name

weather-project

### Dataset

weather_data

### Table

temperature_data

CSV data was uploaded into BigQuery using the BigQuery Sandbox environment.

---

## SQL Query

```sql
SELECT
  AVG(temperature) AS avg_temp,
  MAX(temperature) AS max_temp,
  MIN(temperature) AS min_temp
FROM `weather-project.weather_data.temperature_data`;