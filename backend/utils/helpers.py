from flask import jsonify
from typing import Any, Dict, Tuple, List


def success_response(data: Any, status_code: int = 200):
    """
    Retorna uma resposta de sucesso padronizada
    
    Args:
        data: Dados a serem retornados
        status_code: Código HTTP de status (padrão: 200)
    
    Returns:
        Resposta JSON formatada
    """
    response = {
        'success': True,
        'data': data
    }
    return jsonify(response), status_code


def error_response(message: str, status_code: int = 400, errors: Dict = None):
    """
    Retorna uma resposta de erro padronizada
    
    Args:
        message: Mensagem de erro
        status_code: Código HTTP de status (padrão: 400)
        errors: Detalhes adicionais do erro (opcional)
    
    Returns:
        Resposta JSON formatada
    """
    response = {
        'success': False,
        'error': {
            'message': message,
            'code': status_code
        }
    }
    
    if errors:
        response['error']['details'] = errors
    
    return jsonify(response), status_code


def validate_required_fields(data: Dict, required_fields: List[str]) -> Tuple[bool, str]:
    """
    Valida se todos os campos obrigatórios estão presentes
    
    Args:
        data: Dicionário com os dados a validar
        required_fields: Lista de campos obrigatórios
    
    Returns:
        Tupla (is_valid, message)
    """
    if not data:
        return False, 'Nenhum dado foi fornecido'
    
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        return False, f'Campos obrigatórios ausentes: {", ".join(missing_fields)}'
    
    return True, 'Validação bem-sucedida'


def paginate(items: List, page: int = 1, per_page: int = 10) -> Dict:
    """
    Pagina uma lista de itens
    
    Args:
        items: Lista de itens a paginar
        page: Número da página (começa em 1)
        per_page: Itens por página
    
    Returns:
        Dicionário com dados paginados e metadados
    """
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'items': items[start:end],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    }
