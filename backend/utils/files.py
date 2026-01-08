import os
import glob
from config import get_config

def search_patient_files(prontuario, exam_mapping=None, count_only=False):
    """
    Pesquisa arquivos de um paciente numa pasta específica.
    Padrão: {prontuario}-*
    
    Args:
        prontuario (str): Código do paciente
        exam_mapping (dict, optional): Mapeamento de códigos de exame para descrições.
        count_only (bool): Se True, apenas conta os arquivos (pula leitura de metadados).
    """
    config = get_config()
    found_files = []
    
    # Lista de diretórios para buscar (definidos no config)
    if hasattr(config, 'FILES_BASE_PATHS'):
        base_paths = config.FILES_BASE_PATHS
    elif hasattr(config, 'FILES_BASE_PATH'):
        base_paths = [config.FILES_BASE_PATH]
    else:
        base_paths = []
    
    # print(f"DEBUG: Buscando arquivos para prontuário {prontuario} em: {base_paths}")

    for base_path in base_paths:
        if not os.path.exists(base_path):
            # print(f"DEBUG: Diretório não encontrado ou sem acesso: {base_path}")
            continue

        # Helper para processar arquivo encontrado
        def process_file(f, full_path):
            if count_only:
                return {'name': f} # Mínimo para contagem

            try:
                stat = os.stat(full_path)
            except:
                stat = None
            
            # Análise do nome do arquivo para metadados
            # Padrão esperado: PRONTUARIO-ATEND-DATA-TIPO-OLHO-...
            # Ex: 123-456-20230101-MIC-OD.pdf
            name_parts = f.replace('.pdf', '').replace('.jpg', '').split('-')
            
            display_name = f # Fallback
            exam_type = None
            eye = None
            
            if exam_mapping:
                # Tentar identificar o tipo de exame
                for part in name_parts:
                    part_upper = part.upper().strip()
                    if part_upper in exam_mapping:
                        exam_type = exam_mapping[part_upper]
                    
                    # Identificar olho
                    if part_upper in ['OD', 'OE', 'AO']:
                        eye = part_upper
            
            # Construir nome amigável se conseguiu identificar o tipo
            if exam_type:
                display_name = exam_type
            
            return {
                'name': f, # Nome original para download
                'path': full_path,
                'display_name': display_name,
                'exam_type': exam_type, # Descrição longa
                'eye': eye, # OD, OE, AO
                'size': stat.st_size if stat else 0,
                'date': stat.st_mtime if stat else 0
            }

        # Estratégia 1: Buscar DENTRO de pasta com nome do prontuário
        patient_dir = os.path.join(base_path, prontuario)
        if os.path.isdir(patient_dir):
            try:
                for f in os.listdir(patient_dir):
                    if f.lower().endswith(('.pdf', '.jpg', '.png')):
                        full_path = os.path.join(patient_dir, f)
                        found_files.append(process_file(f, full_path))
            except Exception as e:
                print(f"Erro ao listar diretório {patient_dir}: {e}")

        # Estratégia 2: Buscar NA RAIZ com prefixo
        try:
             # Se for count_only, glob é mais rápido que listdir se houver muitos arquivos
             base_files = glob.glob(os.path.join(base_path, f"{prontuario}*.pdf"))
             for fp in base_files:
                 # Evitar duplicatas (pode ser lento O(N^2), mas N é pequeno por paciente)
                 if count_only:
                      found_files.append({'name': os.path.basename(fp)})
                 elif not any(x['path'] == fp for x in found_files):
                     found_files.append(process_file(os.path.basename(fp), fp))
        except Exception as e:
            print(f"Erro ao buscar glob em {base_path}: {e}")

    # Ordenar por data (mais recente primeiro) - Somente se não for count_only
    if not count_only:
        found_files.sort(key=lambda x: x['date'], reverse=True)
    
    # print(f"DEBUG: Encontrados {len(found_files)} arquivos para {prontuario}")
    return found_files
