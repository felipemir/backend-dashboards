# schemas.py
from pydantic import BaseModel
from typing import List, Optional

# Esquema base para o Dashboard
class Dashboard(BaseModel):
    id: int
    title: str
    type: str
    description: Optional[str] = None
    updatedDate: str
    tags: List[str]
    sector: str
    url: str

    class Config:
        from_attributes = True

# Esquema para exibir dados do usuário
class User(BaseModel):
    id: int
    username: str
    role: str
    sector: Optional[str] = None

    class Config:
        from_attributes = True

# Esquema para a resposta completa do login
class Token(BaseModel):
    token: str
    user: User

# Esquema para os dados dentro do token JWT
class TokenData(BaseModel):
    username: Optional[str] = None