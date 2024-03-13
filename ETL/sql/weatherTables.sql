-- CREAMOS LA TABLA PARA GUARDAR LOS DATOS DE LA API DE WEATHER SQL
CREATE TABLE IF NOT EXISTS jrobertoperezangulo_ipn_coderhouse.weather (
    id SERIAL PRIMARY KEY NOT NULL
    city VARCHAR(100),
    country VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    cloudiness FLOAT,
    date DATE
);

INSERT INTO weather (city, country, latitude, longitude, temperature, humidity, wind_speed, cloudiness, date) VALUES ('CDMX', 'MX', 19.43, -99.13, 20, 50, 10, 20, '2021-10-01');