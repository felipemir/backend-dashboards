# test_db.py
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database import engine, SessionLocal

print("Iniciando teste de conexão com o banco de dados...")

try:
    with engine.connect() as connection:
        # Executa uma consulta SQL muito simples para verificar a conexão.
        # 'SELECT 1' é um comando universal que apenas retorna o número 1.
        result = connection.execute(text("SELECT 1"))
        
        print("✅ Conexão com o banco de dados bem-sucedida!")
        print("   A configuração no seu arquivo .env está correta.")

except SQLAlchemyError as e:
    # Se ocorrer qualquer erro relacionado ao SQLAlchemy (conexão, credenciais, etc.)
    print("❌ Falha ao conectar com o banco de dados.")
    print("   Por favor, verifique os seguintes pontos:")
    print("   1. O servidor MySQL está rodando no endereço especificado?")
    print("   2. A porta (geralmente 3306) está correta e não bloqueada por um firewall?")
    print("   3. O usuário, senha e nome do banco no arquivo .env estão corretos?")
    print("\n--- Detalhes do Erro ---")
    print(e)
    print("------------------------")

except Exception as e:
    # Captura outros erros inesperados (ex: 'mysqlclient' não instalado)
    print("❌ Ocorreu um erro inesperado.")
    print("\n--- Detalhes do Erro ---")
    print(e)
    print("------------------------")