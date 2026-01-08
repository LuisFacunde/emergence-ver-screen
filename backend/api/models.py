from datetime import datetime
from typing import Dict, Any, List, Optional


class BaseModel:
    """Classe base para modelos"""
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o modelo para dicionário"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }


class User(BaseModel):
    """Modelo de usuário de exemplo"""
    
    def __init__(self, id: int, name: str, email: str, created_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = created_at or datetime.now()
    
    def __repr__(self):
        return f"<User {self.name}>"


class Item(BaseModel):
    """Modelo de item de exemplo"""
    
    def __init__(self, id: int, title: str, description: str, created_at: Optional[datetime] = None):
        self.id = id
        self.title = title
        self.description = description
        self.created_at = created_at or datetime.now()
    
    def __repr__(self):
        return f"<Item {self.title}>"


# Dados de exemplo (em produção, usar banco de dados)
users_db: List[User] = [
    User(1, "João Silva", "joao@example.com"),
    User(2, "Maria Santos", "maria@example.com"),
]

items_db: List[Item] = [
    Item(1, "Item 1", "Descrição do item 1"),
    Item(2, "Item 2", "Descrição do item 2"),
    Item(3, "Item 3", "Descrição do item 3"),
]
