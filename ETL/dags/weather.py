from datetime import datetime
from dotenv import load_dotenv

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

from sqlalchemy import create_engine
import psycopg2
from sqlalchemy.orm import sessionmaker
from model.models import Weather, Base

import logging as log
import requests
import os
import pandas as pd

load_dotenv()

engine = create_engine(f"redshift+psycopg2://{os.getenv('user')}:{os.getenv('password')}@{os.getenv('host')}:{os.getenv('port')}/{os.getenv('dbname')}")
Session = sessionmaker(bind=engine)
session = Session()

with DAG(dag_id="weather", start_date=datetime(2024, 3, 1), schedule_interval="@daily", default_args={'retries': 0}) as dag:
    weather = BashOperator(task_id="weather", bash_command="echo weather")

    def tranform_weather(weather_data):
        try:
            # Extracción de los datos como antes
            log.info(weather_data)
            date_time_str = weather_data.get('properties').get('timeseries')[0].get('time')
            data_instant = weather_data.get('properties').get('timeseries')[0].get('data').get('instant').get('details')
            air_temperature = data_instant.get('air_temperature')
            cloud_area_fraction = data_instant.get('cloud_area_fraction')

            # Convierte la cadena de tiempo a un objeto datetime
            date_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%SZ')

            # Prepara el DataFrame para insertar
            df_to_insert = pd.DataFrame({
                'city': ['CDMX'],
                'country': ['MX'],
                'latitude': [19.42847],
                'longitude': [-99.12766],
                'temperature': [air_temperature],
                'humidity': [0], 
                'wind_speed': [0],
                'cloudiness': [cloud_area_fraction],
                'date': [date_time]
            })

            query = "SELECT city, country, date FROM weather;"
            existing_data = pd.read_sql_query(query, engine)

            new_data = pd.merge(df_to_insert, existing_data, on=['city', 'country', 'date'], how='left', indicator=True)
            new_data = new_data[new_data['_merge'] == 'left_only'].drop('_merge', axis=1)

            if not new_data.empty:
                new_data.to_sql('weather', engine, index=False, if_exists='append')
                log.info(f"{len(new_data)} nuevos registros insertados.")
            else:
                log.info("No hay nuevos registros para insertar.")

        except Exception as err:
            log.error(f"An error occurred: {err}")

    @task()
    def fetch_weather():
        try:
            api_key = os.getenv("url")
            url = f"{api_key}/locationforecast/2.0/compact.json"
            params = {'lat':'19.42847','lon':'-99.12766'}
            if not api_key:
                raise ValueError("API key not found")
            print('huevos esta es la URL:', url)
            response = requests.get(url, params=params, timeout=10)
            print('huevos' ,response)
            response.raise_for_status()
            tranform_weather(response.json())
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            log.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
            log.error(f"An error occurred: {err}")

fetch_weather()>>weather