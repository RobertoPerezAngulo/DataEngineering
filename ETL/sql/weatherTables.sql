-- CREAMOS LA TABLA PARA GUARDAR LOS DATOS DE LA API DE WEATHER SQL
CREATE TABLE IF NOT EXISTS weather (
    id SERIAL PRIMARY KEY,
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
