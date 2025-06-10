# crud.py
from sqlalchemy.orm import Session
import models

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_all_dashboards(db: Session):
    return db.query(models.Dashboard).all()

# A consulta para um gestor deve retornar apenas dashboards do seu setor. 
def get_dashboards_by_sector(db: Session, sector: str):
    return db.query(models.Dashboard).filter(models.Dashboard.sector == sector).all()