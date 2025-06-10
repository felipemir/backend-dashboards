# models.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, JSON
from sqlalchemy.sql import func
from database import Base

# Modelo User que representa os usuários que podem acessar o sistema. 
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True) # Identificador único do usuário. 
    username = Column(String(255), unique=True, nullable=False) # Nome de usuário para login. 
    password = Column(String(255), nullable=False) # O hash da senha. 
    role = Column(Enum('secretaria', 'gestor', name='user_roles'), nullable=False) # Nível de permissão do usuário. 
    sector = Column(String(255)) # Setor ao qual o gestor pertence. 
    createdAt = Column(DateTime, server_default=func.now()) # Data de criação do registro. 
    updatedAt = Column(DateTime, onupdate=func.now()) # Data da última atualização. 

# Modelo Dashboard que representa os dashboards a serem exibidos. 
class Dashboard(Base):
    __tablename__ = "dashboards"

    id = Column(Integer, primary_key=True, autoincrement=True) # Identificador único do dashboard. 
    title = Column(String(255), nullable=False) # Título do dashboard. 
    type = Column(Enum('BI', 'REPORT', name='dashboard_types'), nullable=False) # Tipo do item (BI ou Relatório). 
    description = Column(Text) # Breve descrição do dashboard. 
    updatedDate = Column(String(10), nullable=False) # Data da última atualização, no formato "DD/MM/AAAA". 
    tags = Column(JSON, nullable=False) # Tags para facilitar a busca e categorização. 
    sector = Column(String(255), nullable=False) # Setor responsável pelo dashboard. 
    url = Column(String(255), nullable=False)