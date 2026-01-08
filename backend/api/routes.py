from flask import jsonify, request
from . import api_bp
from .models import users_db, items_db, User, Item
from utils.helpers import success_response, error_response, validate_required_fields


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
