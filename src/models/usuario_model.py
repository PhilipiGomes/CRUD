from sqlalchemy import Column, Integer, String
from src import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)