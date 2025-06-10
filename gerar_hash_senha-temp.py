# gerar_hash.py
from auth import get_password_hash
import sys

if len(sys.argv) < 2:
    print("Uso: python gerar_hash.py <senha>")
    sys.exit(1)

senha = sys.argv[1]
hash_da_senha = get_password_hash(senha)
print("Senha em texto plano:", senha)
print("Hash (para o banco):", hash_da_senha)