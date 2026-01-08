from flask import jsonify, request
from . import api_bp
from . import api_bp
from .models import users_db, items_db, User, Item
from utils.helpers import success_response, error_response, validate_required_fields
from utils.database import get_oracle_connection
from utils.files import search_patient_files
import oracledb

@api_bp.route('/files/download', methods=['GET'])
def download_file():
    """
    Faz o download (stream) de um arquivo.
    Query Params:
        - name: Nome do arquivo (apenas para fallback/display)
        - path: Caminho absoluto do arquivo (codificado ou raw)
    """
    from flask import send_file
    from config import get_config
    import os
    
    file_path = request.args.get('path')
    if not file_path:
        return error_response('Caminho do arquivo não informado', 400)
    
    # Decodificar URL se necessário (Flask request.args já decodifica % escapes)
    # Validate security: path must start with one of the allowed FILES_BASE_PATHS
    config = get_config()
    allowed = False
    
    # Normalizar caminhos para comparação segura
    abs_req_path = os.path.abspath(file_path)
    
    for base in config.FILES_BASE_PATHS:
        # Verifica se o caminho requisitado começa com o caminho base permitido
        # os.path.commonpath é seguro para checar subdiretórios
        try:
            if os.path.commonpath([base, abs_req_path]) == os.path.abspath(base):
                allowed = True
                break
        except ValueError:
             # commonpath falha se drives forem diferentes no Windows
             continue
    
    if not allowed:
        print(f"Tentativa de acesso negado: {abs_req_path}")
        return error_response('Acesso a este caminho não é permitido', 403)

    if not os.path.exists(abs_req_path):
        return error_response('Arquivo não encontrado', 404)

    # Verifica se deve forçar download ou apenas visualizar (ex: PDF no navegador)
    force_download = request.args.get('download', 'false').lower() == 'true'

    try:
        # send_file lida com path absoluto se for dado
        return send_file(abs_req_path, as_attachment=force_download)
    except Exception as e:
        return error_response(f"Erro ao ler arquivo: {str(e)}", 404)


@api_bp.route('/patients/search', methods=['GET'])
def search_patients():
    """
    Busca pacientes no Oracle e arquivos relacionados.
    Query Params:
        - prontuario: Código do paciente (cd_paciente)
        - nome: Nome do paciente (nm_paciente)
    """
    import concurrent.futures
    import time

    start_time = time.time()
    prontuario = request.args.get('prontuario', '')
    nome = request.args.get('nome', '')
    
    print(f"DEBUG: Buscando paciente - Prontuario: '{prontuario}', Nome: '{nome}'")
    
    if not prontuario and not nome:
        return error_response('Forneça pelo menos um parâmetro de busca (prontuario ou nome)', 400)
    
    try:
        conn = get_oracle_connection()
        cursor = conn.cursor()
        
        # 1. Buscar Pacientes
        query = """
            SELECT cd_paciente, nm_paciente, to_char(dt_nascimento, 'DD/MM/YYYY') as dt_nascimento 
            FROM paciente 
            WHERE 1=1
        """
        params = {}
        
        if prontuario:
            query += " AND cd_paciente = :prontuario"
            params['prontuario'] = prontuario
            
        if nome:
            query += " AND UPPER(nm_paciente) LIKE UPPER(:nome)"
            params['nome'] = f"%{nome}%"
            
        # Oracle antigo limit
        query += " AND ROWNUM <= 50"
        
        cursor.execute(query, params)
        columns = [col[0].lower() for col in cursor.description]
        rows = cursor.fetchall()
        
        if not rows:
             cursor.close()
             conn.close()
             return success_response([])

        # Converter para lista de dicts
        patients = [dict(zip(columns, row)) for row in rows]
        patient_ids = [p['cd_paciente'] for p in patients]
        
        print(f"DEBUG: Encontrados {len(patients)} pacientes. Tempo DB Pacientes: {time.time() - start_time:.2f}s")
        
        # 2. Busca Paralela de Arquivos
        # Carregar mapeamento de exames (Nome -> Descrição)
        try:
            from utils.database import get_exam_types_mapping
            exam_mapping = get_exam_types_mapping()
            print(f"DEBUG: Carregados {len(exam_mapping)} tipos de exames.")
        except Exception as e:
            print(f"Aviso: Não foi possível carregar tipos de exames: {e}")
            exam_mapping = {}

        file_start_time = time.time()
        
        def fetch_files_for_patient(patient):
            if 'cd_paciente' in patient:
                # OTIMIZAÇÃO MAXIMA: REMOVER contagem de arquivos na busca
                # Listar arquivos em rede (SMB) é lento mesmo só contando.
                # Deixar zerado ou buscar só se necessário.
                # files = search_patient_files(str(patient['cd_paciente']), exam_mapping, count_only=True)
                patient['qtd_exm'] = '-' # Indicador visual de que não contou
                patient['files'] = [] 
                
                # Mapeamento
                patient['prontuario'] = patient['cd_paciente']
                patient['nome'] = patient['nm_paciente']
                # Inicializar campos de atendimento (serão preenchidos depois)
                patient['ultimo_atendimento'] = '-'
                patient['data_ultimo_atendimento'] = '-'
            return patient

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Map mantém a ordem ou podemos iterar depois. Aqui modificamos os dicts in-place/return
            list(executor.map(fetch_files_for_patient, patients))
            
        print(f"DEBUG: Busca de arquivos (contagem) finalizada. Tempo Arquivos: {time.time() - file_start_time:.2f}s")


        # 3. Busca de Atendimentos em Lote (Bulk)
        # Otimização: Buscar último atendimento para todos os IDs de uma vez
        # Compatibilidade Oracle 11g: ROW_NUMBER() é suportado.
        atend_start_time = time.time()
        
        if patient_ids:
            # Construir cláusula IN (:id1, :id2...)
            # Oracle tem limite de 1000 itens no IN, mas limitamos pacientes a 50 na query anterior
            bind_names = [f":id{i}" for i in range(len(patient_ids))]
            bind_dict = {f"id{i}": pid for i, pid in enumerate(patient_ids)}
            
            # Query complexa para pegar o último de cada paciente
            bulk_query = f"""
                SELECT cd_paciente, cd_atendimento, to_char(dt_atendimento, 'DD/MM/YYYY') as dt_atendimento
                FROM (
                    SELECT cd_paciente, cd_atendimento, dt_atendimento,
                           ROW_NUMBER() OVER (PARTITION BY cd_paciente ORDER BY dt_atendimento DESC) as rn
                    FROM atendime
                    WHERE cd_paciente IN ({','.join(bind_names)})
                )
                WHERE rn = 1
            """
            
            try:
                cursor.execute(bulk_query, bind_dict)
                atend_rows = cursor.fetchall()
                
                # Criar mapa para acesso rápido: cd_paciente -> (cd_atend, dt_atend)
                atend_map = {row[0]: (row[1], row[2]) for row in atend_rows}
                
                # Atualizar pacientes
                for p in patients:
                    pid = p['cd_paciente']
                    if pid in atend_map:
                        p['ultimo_atendimento'] = atend_map[pid][0]
                        p['data_ultimo_atendimento'] = atend_map[pid][1]
                        
            except Exception as e:
                print(f"Erro na busca em lote de atendimentos: {e}")
                # Fallback: se falhar o lote, deixar como traço ou tentar individual (melhor deixar traço para não travar)
        
        print(f"DEBUG: Busca atendimentos finalizada. Tempo Atendimentos: {time.time() - atend_start_time:.2f}s")
        
        cursor.close()
        conn.close()
        
        total_time = time.time() - start_time
        print(f"DEBUG: Busca total finalizada em {total_time:.2f}s")
        
        return success_response(patients)
        
    except oracledb.Error as e:
        error_msg = f"Erro de banco de dados: {str(e)}"
        print(error_msg)
        return error_response(error_msg, 500)
    except Exception as e:
        error_msg = f"Erro interno no servidor: {str(e)}"
        print(error_msg)
        # Logar erro completo
        with open('error_log.txt', 'a') as f:
            import traceback
            traceback.print_exc(file=f)
        return error_response(error_msg, 500)

@api_bp.route('/patients/<id>/files', methods=['GET'])
def get_patient_files(id):
    """
    Busca a lista detalhada de arquivos de um paciente.
    """
    try:
        from utils.files import search_patient_files
        
        # Carregar mapping
        exam_mapping = {}
        try:
            from utils.database import get_exam_types_mapping
            exam_mapping = get_exam_types_mapping()
        except:
            pass
            
        files = search_patient_files(id, exam_mapping, count_only=False)
        return success_response(files)
    except Exception as e:
         return error_response(str(e), 500)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return success_response({
        'status': 'healthy',
        'message': 'API está funcionando corretamente'
    })


# ===== USERS ENDPOINTS =====

@api_bp.route('/users', methods=['GET'])
def get_users():
    """Retorna todos os usuários"""
    users = [user.to_dict() for user in users_db]
    return success_response(users)


@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retorna um usuário específico"""
    user = next((u for u in users_db if u.id == user_id), None)
    
    if not user:
        return error_response('Usuário não encontrado', 404)
    
    return success_response(user.to_dict())


@api_bp.route('/users', methods=['POST'])
def create_user():
    """Cria um novo usuário"""
    data = request.get_json()
    
    # Validação
    required_fields = ['name', 'email']
    is_valid, message = validate_required_fields(data, required_fields)
    if not is_valid:
        return error_response(message, 400)
    
    # Criar novo usuário
    new_id = max([u.id for u in users_db], default=0) + 1
    new_user = User(new_id, data['name'], data['email'])
    users_db.append(new_user)
    
    return success_response(new_user.to_dict(), 201)


@api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Atualiza um usuário existente"""
    user = next((u for u in users_db if u.id == user_id), None)
    
    if not user:
        return error_response('Usuário não encontrado', 404)
    
    data = request.get_json()
    
    # Atualizar campos
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    
    return success_response(user.to_dict())


@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Remove um usuário"""
    global users_db
    user = next((u for u in users_db if u.id == user_id), None)
    
    if not user:
        return error_response('Usuário não encontrado', 404)
    
    users_db = [u for u in users_db if u.id != user_id]
    
    return success_response({'message': 'Usuário removido com sucesso'})


# ===== ITEMS ENDPOINTS =====

@api_bp.route('/items', methods=['GET'])
def get_items():
    """Retorna todos os itens"""
    items = [item.to_dict() for item in items_db]
    return success_response(items)


@api_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Retorna um item específico"""
    item = next((i for i in items_db if i.id == item_id), None)
    
    if not item:
        return error_response('Item não encontrado', 404)
    
    return success_response(item.to_dict())


@api_bp.route('/items', methods=['POST'])
def create_item():
    """Cria um novo item"""
    data = request.get_json()
    
    # Validação
    required_fields = ['title', 'description']
    is_valid, message = validate_required_fields(data, required_fields)
    if not is_valid:
        return error_response(message, 400)
    
    # Criar novo item
    new_id = max([i.id for i in items_db], default=0) + 1
    new_item = Item(new_id, data['title'], data['description'])
    items_db.append(new_item)
    
    return success_response(new_item.to_dict(), 201)


@api_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Atualiza um item existente"""
    item = next((i for i in items_db if i.id == item_id), None)
    
    if not item:
        return error_response('Item não encontrado', 404)
    
    data = request.get_json()
    
    # Atualizar campos
    if 'title' in data:
        item.title = data['title']
    if 'description' in data:
        item.description = data['description']
    
    return success_response(item.to_dict())


@api_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Remove um item"""
    global items_db
    item = next((i for i in items_db if i.id == item_id), None)
    
    if not item:
        return error_response('Item não encontrado', 404)
    
    items_db = [i for i in items_db if i.id != item_id]
    
    return success_response({'message': 'Item removido com sucesso'})
