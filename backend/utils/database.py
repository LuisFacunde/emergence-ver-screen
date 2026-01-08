import oracledb
from config import get_config

# Tentar inicializar o cliente Oracle (Thick Mode) globalmente
try:
    oracledb.init_oracle_client()
    with open("init_log.txt", "a") as f:
        f.write("Oracle Client initialized successfully.\n")
except Exception as e:
    with open("init_log.txt", "a") as f:
        f.write(f"Oracle Client initialization warning/error: {e}\n")

def get_oracle_connection():
    """
    Estabelece conexão com o banco de dados Oracle.
    """
    # Carregar configuração
    config = get_config()
    
    # Construir DSN (Data Source Name)
    dsn = f"{config.ORACLE_HOST}:{config.ORACLE_PORT}/{config.ORACLE_SERVICE}"
    
    try:
        # Conectar
        connection = oracledb.connect(
            user=config.ORACLE_USER,
            password=config.ORACLE_PASSWORD,
            dsn=dsn
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar no Oracle: {e}")
        log_init_result(f"Failed to connect: {e}")
        raise e

def get_exam_types_mapping():
    """
    Retorna um dicionário mapeando nome_exame -> tipo.
    Ex: {'MIC': 'Microscopia', 'BIO': 'Biometria'}
    """
    mapping = {}
    conn = None
    try:
        conn = get_oracle_connection()
        cursor = conn.cursor()
        # Selecionar campos relevantes
        cursor.execute("SELECT nome_exame, tipo FROM exames")
        rows = cursor.fetchall()
        for row in rows:
            if row[0] and row[1]:
                # Chave: codigo do exame (nome_exame), Valor: descrição (tipo)
                mapping[row[0].strip().upper()] = row[1].strip()
        cursor.close()
    except Exception as e:
        print(f"Erro ao buscar tipos de exames: {e}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass
    return mapping
