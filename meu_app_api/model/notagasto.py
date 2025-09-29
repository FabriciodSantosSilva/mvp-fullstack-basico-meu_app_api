from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from model.base import Base


class NotaGasto(Base):
    __tablename__ = 'nota_gasto'

    id = Column(Integer, primary_key=True)
    # Texto da anotação/detalhe
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento: Chave Estrangeira que aponta para 'gasto'.
    gasto = Column(Integer, ForeignKey("gasto.pk_gasto"), nullable=False)

    def __init__(self, texto:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Nota de Gasto (Comentário/Observação)

        Arguments:
            texto: o texto da nota.
            data_insercao: data de quando a nota foi feita ou inserida.
        """
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao