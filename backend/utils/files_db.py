import os
import time
from config import get_config
from utils.database import get_oracle_connection
import oracledb

# Cache global para resultados de busca
_file_cache = {}
_cache_ttl = 300  # 5 minutos

def clear_file_cache():
    """Limpa o cache de arquivos"""
    global _file_cache
    _file_cache = {}
    print("Cache de arquivos limpo")

def search_patient_files(prontuario, exam_mapping=None, count_only=False):
    """
    Pesquisa arquivos de um paciente consultando a tabela anexos_exames.
    
    Args:
        prontuario (str): Código do paciente
        exam_mapping (dict, optional): Mapeamento de IDs/Códigos de exame para descrições.
        count_only (bool): Se True, retorna lista simplificada (não usado na rota detalhada).
    """
    # Verificar cache
    cache_key = f"{prontuario}_{count_only}_db"
    current_time = time.time()
    
    if cache_key in _file_cache:
        cached_data, cache_time = _file_cache[cache_key]
        if current_time - cache_time < _cache_ttl:
            # print(f"DEBUG: Retornando do cache para {prontuario}")
            return cached_data

    files = []
    conn = None
    try:
        conn = get_oracle_connection()
        cursor = conn.cursor()
        
        # Selecionar caminhos e metadados
        # statusdoc: A=Assinado, B=Bloqueado, E=Excluido
        # Filtramos apenas 'A'
        query = """
            SELECT caminho_anexo, caminho_anexo_rede2, procedimento, olho, statusdoc, DATA, observacoes
            FROM anexos_exames
            WHERE prontuario = :prontuario
              AND statusdoc = 'A'
        """
        
        cursor.execute(query, {'prontuario': prontuario})
        rows = cursor.fetchall()
        
        for row in rows:
            # colunas: 
            # 0: caminho_anexo (4.18)
            # 1: caminho_anexo_rede2 (4.52)
            # 2: procedimento (ID)
            # 3: olho
            # 4: statusdoc
            # 5: DATA (datetime)
            # 6: observacoes (str)
            
            path_418 = row[0]
            path_452 = row[1]
            proc_id = row[2]
            eye = row[3]
            data_db = row[5]
            obs = row[6]
            
            selected_path = None
            
            # Prioridade 1: 4.18 (caminho_anexo)
            if path_418 and os.path.exists(path_418):
                selected_path = path_418
            # Prioridade 2: 4.52 (caminho_anexo_rede2)
            elif path_452 and os.path.exists(path_452):
                selected_path = path_452
                
            # Se encontrou um caminho válido
            if selected_path:
                # Determinar display name
                display_name = str(proc_id)
                exam_type = None
                
                if exam_mapping:
                    # Tentar mapear pelo ID (numérico)
                    if proc_id in exam_mapping:
                        exam_type = exam_mapping[proc_id]
                        display_name = exam_type
                    # Fallback para string se necessário (embora procedimento seja number)
                    elif str(proc_id) in exam_mapping:
                        exam_type = exam_mapping[str(proc_id)]
                        display_name = exam_type

                # Metadados de data
                timestamp = 0
                if data_db:
                    try:
                        timestamp = data_db.timestamp()
                    except:
                        pass
                
                # Tamanho
                try:
                    size = os.path.getsize(selected_path)
                except:
                    size = 0
                
                files.append({
                    'name': os.path.basename(selected_path),
                    'path': selected_path,
                    'display_name': display_name,
                    'exam_type': exam_type,
                    'eye': eye,
                    'size': size,
                    'date': timestamp,
                    'file_date': timestamp,
                    'observation': obs if obs else ''
                })
        
        cursor.close()
        
        # Cache results
        _file_cache[cache_key] = (files, current_time)
        return files

    except Exception as e:
        print(f"Erro ao buscar arquivos via DB para {prontuario}: {e}")
        # Log error
        try:
             with open("error_log.txt", "a") as f:
                f.write(f"DB Search Error ({prontuario}): {e}\n")
        except:
            pass
        return []
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass
