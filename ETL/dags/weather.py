from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
import requests
import logging as log

with DAG(dag_id="weather", start_date=datetime(2024, 3, 1), schedule_interval="0 0 * * *") as dag:
    weather = BashOperator(task_id="weather", bash_command="echo weather")


    def tranform_weather(weather_data):
        try:
            log.info(weather_data)
            date_time = weather_data.get('properties').get('timeseries')[0].get('time')
            data_instant = weather_data.get('properties').get('timeseries')[0].get('data').get('instant').get('details')
            air_temperature = data_instant.get('air_temperature')
            cloud_area_fraction = data_instant.get('cloud_area_fraction')
            print(f"Date and time: {date_time}")
            print(f"Air temperature: {air_temperature}")
            print(f"Cloud area fraction: {cloud_area_fraction}")
            return date_time
        except Exception as err:
            log.error(f"An error occurred: {err}")


    @task()
    def fetch_weather():
        try:
            response = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/compact.json?lat=19.42847&lon=-99.12766')
            response.raise_for_status()
            print(response.json())
            tranform_weather(response.json())
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            log.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            log.error(f"An error occurred: {err}")
    
    fetch_weather() >> weather