import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuração base da aplicação"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    
    # Server
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')

    # Oracle Database
    ORACLE_HOST = os.getenv('ORACLE_HOST', '192.168.4.90')
    ORACLE_PORT = os.getenv('ORACLE_PORT', '1521')
    ORACLE_SERVICE = os.getenv('ORACLE_SERVICE', 'prd')
    ORACLE_USER = os.getenv('ORACLE_USER', 'dbamv')
    ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD', 'fav1983db2')
    
    # File System
    # Suporte a múltiplos caminhos separados por ponto e vírgula (;)
    # Ex: \\server1\share;\\server2\share\subdir
    _files_env = os.getenv('FILES_BASE_PATH', r'\\192.168.4.52\c$\exames;\\192.168.4.18\c$\apache24\htdocs\fav_exames\anexo')
    FILES_BASE_PATHS = [p.strip() for p in _files_env.split(';') if p.strip()]


class DevelopmentConfig(Config):
    """Configuração para ambiente de desenvolvimento"""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """Configuração para ambiente de produção"""
    DEBUG = False
    ENV = 'production'


class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    DEBUG = True


# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Retorna a configuração baseada na variável de ambiente FLASK_ENV"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
