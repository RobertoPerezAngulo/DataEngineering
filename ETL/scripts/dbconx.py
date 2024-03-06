from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Parámetros de conexión
database = os.getenv("data-engineer-database")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")

# Cadena de conexión SQLAlchemy para Redshift
conn_string = f"redshift+psycopg2://{user}:{password}@{host}:{port}/{database}"

# Crear motor y sesión
engine = create_engine(conn_string)
Session = sessionmaker(bind=engine)
session = Session()

# Ejemplo de consulta con SQLAlchemy ORM
# Asegúrate de tener definidos los modelos de tus tablas según la documentación de SQLAlchemy
# results = session.query(YourModel).limit(10).all()

# No olvides cerrar la sesión
session.close()
