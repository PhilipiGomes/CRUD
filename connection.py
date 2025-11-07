import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
USER = os.getenv("USER")
SQLALCHEMY_DATABASE_URI = (
    f"mysql://'{USER}':{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = True

# teste de conexão

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    print("banco conectado")
except Exception as e:
    print(f"falha ao conectar {e}")
