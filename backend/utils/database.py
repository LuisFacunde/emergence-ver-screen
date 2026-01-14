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
        # Selecionar campos relevantes: id (conforme usuario), nome_exame (cod string), tipo (descricao)
        # Assumindo que a coluna de ID é 'id' conforme solicitado.
        # Se 'id' não existir, isso falhará. Mas vamos confiar na instrução.
        cursor.execute("SELECT id, nome_exame, tipo FROM exames")
        rows = cursor.fetchall()
        for row in rows:
            # row[0] = id (numeric)
            # row[1] = nome_exame (string code)
            # row[2] = tipo (description)
            exam_id = row[0]
            code = row[1]
            desc = row[2]
            
            if desc:
                clean_desc = desc.strip()
                # Mapear pelo ID (para busca na tabela anexos_exames)
                if exam_id is not None:
                    mapping[exam_id] = clean_desc
                
                # Manter mapeamento antigo por segurança (pelo código string)
                if code:
                    mapping[code.strip().upper()] = clean_desc
                    
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
