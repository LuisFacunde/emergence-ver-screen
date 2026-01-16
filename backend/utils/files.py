import os
import glob
from config import get_config
from functools import lru_cache
import time
import concurrent.futures

# Cache global para resultados de busca (TTL de 5 minutos)
_file_cache = {}
_cache_ttl = 300  # 5 minutos

def clear_file_cache():
    """Limpa o cache de arquivos"""
    global _file_cache
    _file_cache = {}
    print("Cache de arquivos limpo")

def _search_in_server(base_path, prontuario, exam_mapping, count_only):
    found_files = []
    seen_names = set()

    if not os.path.exists(base_path):
        return found_files, False

    EXT_VALIDAS = {'.pdf', '.jpg', '.png'}

    def process_file(entry):
        name = entry.name

        if count_only:
            return {'name': name}

        try:
            stat = entry.stat()
            file_mtime = stat.st_mtime
            size = stat.st_size
        except:
            file_mtime = 0
            size = 0

        name_no_ext, _ = os.path.splitext(name)
        parts = name_no_ext.split('-')

        display_name = name
        exam_type = None
        eye = None
        date_from_filename = None

        # Extrair data YYYYMMDD
        if len(parts) >= 3:
            date_str = parts[2]
            if date_str.isdigit() and len(date_str) == 8:
                try:
                    import datetime
                    date_from_filename = datetime.datetime.strptime(
                        date_str, "%Y%m%d"
                    ).timestamp()
                except:
                    pass

        if exam_mapping:
            for part in parts:
                p = part.upper()
                if p in exam_mapping:
                    exam_type = exam_mapping[p]
                elif p in ('OD', 'OE', 'AO'):
                    eye = p

        if exam_type:
            display_name = exam_type

        return {
            'name': name,
            'path': entry.path,
            'display_name': display_name,
            'exam_type': exam_type,
            'eye': eye,
            'size': size,
            'date': date_from_filename or file_mtime,
            'file_date': file_mtime
        }

    # ==========================
    # Estratégia 1 — pasta do paciente
    # ==========================
    patient_dir = os.path.join(base_path, prontuario)
    start = time.time()

    if os.path.isdir(patient_dir):
        try:
            with os.scandir(patient_dir) as entries:
                for entry in entries:
                    if not entry.is_file():
                        continue

                    _, ext = os.path.splitext(entry.name)
                    if ext.lower() not in EXT_VALIDAS:
                        continue

                    if entry.name not in seen_names:
                        found_files.append(process_file(entry))
                        seen_names.add(entry.name)

            print(
                f"DEBUG: [{base_path}] Estratégia 1 encontrou "
                f"{len(found_files)} arquivos em {time.time() - start:.2f}s"
            )
        except Exception as e:
            print(f"Erro ao listar {patient_dir}: {e}")

    if found_files:
        return found_files, False

    # ==========================
    # Estratégia 2 — raiz com prefixo
    # ==========================
    start = time.time()
    try:
        with os.scandir(base_path) as entries:
            for entry in entries:
                if not entry.is_file():
                    continue

                if not entry.name.startswith(prontuario + '-'):
                    continue

                _, ext = os.path.splitext(entry.name)
                if ext.lower() not in EXT_VALIDAS:
                    continue

                if entry.name not in seen_names:
                    found_files.append(process_file(entry))
                    seen_names.add(entry.name)

        print(
            f"DEBUG: [{base_path}] Estratégia 2 finalizada "
            f"em {time.time() - start:.2f}s"
        )
    except Exception as e:
        print(f"Erro ao buscar em {base_path}: {e}")

    return found_files, False

    """
    Busca arquivos em um servidor específico.
    Esta função é executada em paralelo para cada servidor.
    """
    found_files = []
    
    if not os.path.exists(base_path):
        return found_files, False  # files, partial_result
    
    # Helper para processar arquivo encontrado
    def process_file(f, full_path):
        if count_only:
            return {'name': f}

        try:
            stat = os.stat(full_path)
            file_mtime = stat.st_mtime
        except:
            stat = None
            file_mtime = 0
        
        # Análise do nome do arquivo para metadados
        name_parts = f.replace('.pdf', '').replace('.jpg', '').replace('.png', '').split('-')
        
        display_name = f
        exam_type = None
        eye = None
        date_from_filename = None
        
        # Tentar extrair data do nome do arquivo (formato: PRONTUARIO-ATEND-YYYYMMDD-TIPO-OLHO)
        if len(name_parts) >= 3:
            date_str = name_parts[2]
            if date_str and len(date_str) == 8 and date_str.isdigit():
                try:
                    year = int(date_str[0:4])
                    month = int(date_str[4:6])
                    day = int(date_str[6:8])
                    # Converter para timestamp para ordenação
                    import datetime
                    date_from_filename = datetime.datetime(year, month, day).timestamp()
                except:
                    pass
        
        if exam_mapping:
            for part in name_parts:
                part_upper = part.upper().strip()
                if part_upper in exam_mapping:
                    exam_type = exam_mapping[part_upper]
                
                if part_upper in ['OD', 'OE', 'AO']:
                    eye = part_upper
        
        if exam_type:
            display_name = exam_type
        
        return {
            'name': f,
            'path': full_path,
            'display_name': display_name,
            'exam_type': exam_type,
            'eye': eye,
            'size': stat.st_size if stat else 0,
            'date': date_from_filename if date_from_filename else file_mtime,  # Prioriza data do nome
            'file_date': file_mtime  # Mantém data do arquivo para referência
        }

    # Estratégia 1: Buscar DENTRO de pasta com nome do prontuário
    # Esta é a estratégia mais rápida e correta se a pasta existir.
    patient_dir = os.path.join(base_path, prontuario)
    start_s1 = time.time()
    if os.path.isdir(patient_dir):
        try:
            for pattern in ['*.pdf', '*.jpg', '*.png', '*.PDF', '*.JPG', '*.PNG']:
                for full_path in glob.iglob(os.path.join(patient_dir, pattern)):
                    f = os.path.basename(full_path)
                    found_files.append(process_file(f, full_path))
            print(f"DEBUG: [{base_path}] Estratégia 1 (pasta direta) encontrou {len(found_files)} arquivos em {time.time() - start_s1:.2f}s")
        except Exception as e:
            print(f"Erro ao listar diretório {patient_dir}: {e}")

    # OTIMIZAÇÃO: Se encontrou arquivos na pasta do paciente, NÃO buscar na raiz.
    # Assumimos que se a pasta existe, os arquivos estão lá.
    if found_files:
        print(f"DEBUG: [{base_path}] Pulando Estratégia 2 pois arquivos foram encontrados na pasta do paciente.")
        return found_files, False # Completly success

    # Estratégia 2: Buscar NA RAIZ com prefixo
    # Isso é muito lento em shares de rede grandes.
    start_s2 = time.time()
    try:
        # Check rápido se existe pelo menos um arquivo antes de iterar tudo (opcional, pode ser lento também)
        # Vamos restringir a busca para evitar timeout se possível
        
        for pattern in ['*.pdf', '*.PDF', '*.jpg', '*.JPG', '*.png', '*.PNG']:
            # Verificar timeout implícito/cancelamento seria bom aqui, mas glob é bloqueante
            search_pattern = os.path.join(base_path, f"{prontuario}-{pattern}")
            for fp in glob.iglob(search_pattern):
                f = os.path.basename(fp)
                # Evitar duplicatas dentro do mesmo servidor
                if not any(x.get('name') == f for x in found_files):
                    if count_only:
                        found_files.append({'name': f})
                    else:
                        found_files.append(process_file(f, fp))
        print(f"DEBUG: [{base_path}] Estratégia 2 (glob raiz) finalizada em {time.time() - start_s2:.2f}s")
    except Exception as e:
        print(f"Erro ao buscar glob em {base_path}: {e}")
    
    return found_files, False

def search_patient_files(prontuario, exam_mapping=None, count_only=False):
    """
    Pesquisa arquivos de um paciente numa pasta específica.
    Padrão: {prontuario}-*
    
    Args:
        prontuario (str): Código do paciente
        exam_mapping (dict, optional): Mapeamento de códigos de exame para descrições.
        count_only (bool): Se True, apenas conta os arquivos (pula leitura de metadados).
    """
    # Verificar cache
    cache_key = f"{prontuario}_{count_only}"
    current_time = time.time()
    
    if cache_key in _file_cache:
        cached_data, cache_time = _file_cache[cache_key]
        if current_time - cache_time < _cache_ttl:
            print(f"DEBUG: Retornando do cache para {prontuario}")
            return cached_data
    
    config = get_config()
    
    # Lista de diretórios para buscar (definidos no config)
    if hasattr(config, 'FILES_BASE_PATHS'):
        base_paths = config.FILES_BASE_PATHS
    elif hasattr(config, 'FILES_BASE_PATH'):
        base_paths = [config.FILES_BASE_PATH]
    else:
        base_paths = []
    
    print(f"DEBUG: Buscando em {len(base_paths)} servidores em paralelo para {prontuario}")
    
    # OTIMIZAÇÃO: Buscar em paralelo em todos os servidores
    all_files = []
    seen_filenames = set()
    has_timeout = False
    
    # Timeout aumentado para 30s total (era 10s) e 15s por tarefa (era 5s)
    TIMEOUT_PER_TASK = 15
    TIMEOUT_GLOBAL = 30
    
    # Usar ThreadPoolExecutor para buscar em paralelo com TIMEOUT
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(base_paths)) as executor:
        # Submeter busca para cada servidor
        future_to_server = {
            executor.submit(_search_in_server, base_path, prontuario, exam_mapping, count_only): base_path
            for base_path in base_paths
        }
        
        # Processar resultados conforme ficam prontos (COM TIMEOUT)
        try:
            for future in concurrent.futures.as_completed(future_to_server, timeout=TIMEOUT_GLOBAL):
                server = future_to_server[future]
                try:
                    # Timeout por servidor
                    server_files, partial = future.result(timeout=TIMEOUT_PER_TASK)
                    print(f"DEBUG: Servidor {server}: {len(server_files)} arquivos encontrados")
                    
                    if partial:
                        has_timeout = True
                    
                    # Adicionar apenas arquivos únicos
                    for file_data in server_files:
                        filename = file_data.get('name')
                        if filename not in seen_filenames:
                            all_files.append(file_data)
                            seen_filenames.add(filename)
                        else:
                            print(f"DEBUG: DUPLICATA IGNORADA: {filename} (já existe de outro servidor)")
                except concurrent.futures.TimeoutError:
                    print(f"AVISO: Timeout ao buscar em {server} (> {TIMEOUT_PER_TASK}s) - servidor ignorado ou interrompido")
                    has_timeout = True
                except Exception as e:
                    print(f"Erro ao buscar em {server}: {e}")
                    # Erro de IO não deve impedir cache, mas timeout sim
        except concurrent.futures.TimeoutError:
            print(f"AVISO: Timeout global (> {TIMEOUT_GLOBAL}s) - processando arquivos encontrados até agora")
            has_timeout = True

    # Ordenar por data (mais recente primeiro) - Somente se não for count_only
    if not count_only and all_files:
        all_files.sort(key=lambda x: x.get('date', 0), reverse=True)
        print(f"DEBUG: Arquivos ordenados por data (mais recente primeiro)")
        if all_files:
            print(f"DEBUG: Primeiro arquivo: {all_files[0].get('name')} - Data: {all_files[0].get('date')}")
    
    # Armazenar no cache SOMENTE SE NÃO HOUVE TIMEOUT
    # Isso evita cachear "sem arquivos" quando na verdade o servidor só estava lento
    if not has_timeout:
        _file_cache[cache_key] = (all_files, current_time)
        print(f"DEBUG: Resultado cacheado para {prontuario}")
    else:
        print(f"DEBUG: Resultado NÃO cacheado devido a timeout parcial")
    
    print(f"DEBUG: Total de {len(all_files)} arquivos únicos para {prontuario}")
    return all_files
