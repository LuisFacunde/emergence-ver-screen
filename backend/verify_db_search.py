from utils.files import search_patient_files
from utils.database import get_exam_types_mapping, get_oracle_connection
import time

def verify():
    print("Iniciando verificação de busca via Banco de Dados...")
    
    # 1. Testar conexão e mapping
    print("1. Buscando mapping de exames...")
    try:
        mapping = get_exam_types_mapping()
        print(f"Mapping carregado: {len(mapping)} itens")
        if mapping:
            first_key = next(iter(mapping))
            print(f"Exemplo: {first_key} -> {mapping[first_key]}")
    except Exception as e:
        print(f"Erro ao carregar mapping: {e}")
        return

    # 2. Encontrar um prontuário válido para teste
    print("\n2. Buscando um prontuário com exames na tabela anexos_exames...")
    prontuario = '2209394' # Tentar o do histórico
    
    try:
        conn = get_oracle_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT prontuario FROM anexos_exames WHERE statusdoc = 'A' AND ROWNUM = 1")
        row = cursor.fetchone()
        if row:
            prontuario_db = row[0]
            print(f"Encontrado prontuário aleatório na tabela: {prontuario_db}")
            prontuario = str(prontuario_db)
        else:
            print(f"Nenhum registro encontrado em anexos_exames. Usando fallback {prontuario}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao buscar prontuário: {e}")

    # 3. Executar busca via utils.files
    print(f"\n3. Buscando arquivos para prontuário {prontuario}...")
    start = time.time()
    files = search_patient_files(prontuario, mapping, count_only=False)
    duration = time.time() - start
    
    print(f"Busca finalizada em {duration:.2f}s")
    print(f"Total de arquivos encontrados: {len(files)}")
    
    if files:
        print("\nLista de arquivos (primeiros 5):")
        for f in files[:5]:
            print(f" - {f['display_name']} ({f['exam_type']}): {f['name']}")
            print(f"   Path: {f['path']}")
            print(f"   Size: {f['size']}")
            print(f"   Date: {f['date']}")
            print("-" * 20)
    else:
        print("Nenhum arquivo retornado. Verifique se o caminho existe no servidor ou se o usuário tem permissão.")

if __name__ == "__main__":
    verify()
