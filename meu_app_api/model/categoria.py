import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy_utils import UUIDType
from model.base import Base


class Categoria(Base):
    __tablename__ = 'categoria'

    # Identificador único gerado automaticamente como UUID (Universally Unique Identifiers)
    id = Column("pk_categoria", UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    # O nome da categoria (e.g., 'Alimentação', 'Transporte')
    nome = Column(String(100), unique=True, nullable=False)
    # Campo opcional para definir a ordem de exibição das categorias
    ordem = Column(Integer)

    def __init__(self, nome: str, ordem: int = None):
        """
        Cria uma Categoria

        Arguments:
            nome: Nome da categoria (deve ser único).
            ordem: Ordem de exibição (opcional).
        """
        self.nome = nome
        self.ordem = ordem
        