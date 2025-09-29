import uuid
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from datetime import datetime
from typing import Union

# Importando a Base (e as outras classes, se necessário)
from model.base import Base


class Gasto(Base):
    __tablename__ = 'gasto'

    # Identificador único gerado automaticamente como UUID (Universally Unique Identifiers)
    id = Column("pk_gasto", UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    descricao = Column(String(140))
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())
    data_gasto = Column(DateTime, default=datetime.now())

    # 1. CHAVE ESTRANGEIRA para a tabela 'categoria'
    # Esta coluna armazena o ID da categoria
    #categoria_id = Column(Integer, ForeignKey('categoria.pk_categoria'), nullable=False)
    categoria_id = Column(UUIDType(binary=False), ForeignKey('categoria.pk_categoria'), nullable=False)

    # 2. RELACIONAMENTO com a classe Categoria
    # Este objeto permite carregar a categoria completa (objeto Categoria)
    # O 'back_populates' conecta as duas classes.
    categoria_obj = relationship("Categoria")

    # notas = relationship("NotaGasto") # Descomente após criar a classe NotaGasto

    def __init__(self, descricao: str, valor: float, categoria_id: int,
                 data_gasto: Union[DateTime, None] = None, data_insercao: Union[DateTime, None] = None):
        """
        Cria um registro de Gasto

        Arguments:
            descricao: Descrição breve do gasto.
            valor: Valor total do gasto.
            categoria_id: O ID da Categoria a que este gasto pertence.
            data_gasto: Data em que o gasto realmente ocorreu.
            data_insercao: Data de quando o registro foi inserido à base.
        """
        self.descricao = descricao
        self.valor = valor
        # Agora o Gasto é inicializado com o ID da categoria
        self.categoria_id = categoria_id

        if data_gasto:
            self.data_gasto = data_gasto

        if data_insercao:
            self.data_insercao = data_insercao