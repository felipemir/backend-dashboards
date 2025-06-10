# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from jose import JWTError, jwt

import models, schemas, crud, auth
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Dashboards",
              description="API para gerenciar dashboards com autenticação de usuários.",)

# Lista de origens permitidas
origins =[
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)


# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,   
        detail="Credenciais inválidas.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica o token JWT para extrair as informações do usuário (role e sector). 
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Endpoint: POST /api/auth/login 
# Autentica um usuário e retorna um token de acesso. 
@app.post("/api/auth/login", response_model=schemas.Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas."
        )
    
    # O payload do JWT deve conter, no mínimo, role e sector. 
    token_data = {"sub": user.username, "role": user.role, "sector": user.sector}
    access_token = auth.create_access_token(data=token_data)

    user_data_for_response = schemas.User.from_orm(user)

    return {"token": access_token, "user": user_data_for_response}

# Endpoint: GET /api/dashboards 
# Retorna uma lista de dashboards com base no perfil do usuário. 
@app.get("/api/dashboards", response_model=List[schemas.Dashboard])
def read_dashboards(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Se role for 'secretaria', retorna todos os dashboards. 
    if current_user.role == 'secretaria':
        return crud.get_all_dashboards(db=db)
    
    # Se role for 'gestor', retorna apenas os dashboards onde o dashboard.sector corresponda ao user.sector. 
    if current_user.role == 'gestor':
        return crud.get_dashboards_by_sector(db=db, sector=current_user.sector)
    
    raise HTTPException(status_code=403, detail="Acesso não autorizado.")