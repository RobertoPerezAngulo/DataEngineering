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

load_dotenv()

engine = create_engine(f"redshift+psycopg2://{os.getenv('user')}:{os.getenv('password')}@{os.getenv('host')}:{os.getenv('port')}/{os.getenv('dbname')}")
Session = sessionmaker(bind=engine)
session = Session()

with DAG(dag_id="weather", start_date=datetime(2024, 3, 1), schedule_interval="*/10 * * * *") as dag:
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

            conn = psycopg2.connect(
                dbname=os.getenv('dbname'),
                user=os.getenv('user'),
                password=os.getenv('password'),
                host=os.getenv('host'),
                port=os.getenv('port')
            )
            cursor = conn.cursor()

            insert_query = """
            INSERT INTO weather (city, country, latitude, longitude, temperature, humidity, wind_speed, cloudiness, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            
            # Valores a insertar
            data = (
                'CDMX', 'MX', 19.42847, -99.12766, air_temperature, 0, 0, cloud_area_fraction, date_time
            )
            cursor.execute(insert_query, data)
            conn.commit()
            cursor.close()
            conn.close()

            weather_records = session.query(Weather).all()
            for record in weather_records:
                print(str(record.city),str(record.temperature))
            return date_time
        except Exception as err:
            print(err)
            log.error(f"An error occurred: {err}")


    @task()
    def fetch_weather():
        try:
            api_key = os.getenv("url")
            print(api_key)
            if not api_key:
                raise ValueError("API key not found")
            response = requests.get(f'{api_key}/locationforecast/2.0/compact.json?lat=19.42847&lon=-99.12766',timeout=10)
            response.raise_for_status()
            tranform_weather(response.json())
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            log.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
            log.error(f"An error occurred: {err}")
    
    fetch_weather() >> weather