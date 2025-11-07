import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Variáveis de configuração
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT", "3306")  # Define o valor padrão para a porta, caso não esteja definido no .env
PASSWORD = os.getenv("PASSWORD", "")  # Defina o valor padrão para a senha, caso esteja em branco
HOST = os.getenv("HOST", "localhost")  # Define o valor padrão para o host
USER = os.getenv("USER", "root")  # Define o valor padrão para o usuário

# Conexão com o banco de dados
SQLALCHEMY_DATABASE_URI = (
    f"mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desabilitar a modificação de rastreamento, para melhorar performance

# Teste de conexão (se desejado)
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    print("Banco de dados conectado com sucesso")
except Exception as e:
    print(f"Falha ao conectar ao banco: {e}")
