from flask import Flask, jsonify
from flask_cors import CORS
from config import get_config
from api import api_bp


def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Carregar configurações
    config = get_config()
    app.config.from_object(config)
    
    # Configurar CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Registrar blueprints
    app.register_blueprint(api_bp)
    
    # Rota raiz
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Backend Flask - API funcionando!',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'users': '/api/users',
                'items': '/api/items'
            }
        })
    
    # Tratamento de erro 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': {
                'message': 'Endpoint não encontrado',
                'code': 404
            }
        }), 404
    
    # Tratamento de erro 500
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': {
                'message': 'Erro interno do servidor',
                'code': 500
            }
        }), 500
    
    # Tratamento de erro 405 (método não permitido)
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': {
                'message': 'Método HTTP não permitido',
                'code': 405
            }
        }), 405
    
    return app


if __name__ == '__main__':
    app = create_app()
    config = get_config()
    
    print(f"\n{'='*50}")
    print(f"🚀 Servidor Flask iniciando...")
    print(f"{'='*50}")
    print(f"Ambiente: {config.ENV}")
    print(f"Debug: {config.DEBUG}")
    print(f"URL: http://{config.HOST}:{config.PORT}")
    print(f"{'='*50}\n")
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
