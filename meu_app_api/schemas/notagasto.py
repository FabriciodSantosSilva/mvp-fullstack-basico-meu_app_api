from datetime import datetime
from pydantic import BaseModel

class NotaGastoSchema(BaseModel):
    """ Schema para inserção de uma nova NotaGasto (texto). """
    texto: str


class NotaGastoViewSchema(BaseModel):
    """ Schema para retorno/visualização de uma NotaGasto. """
    id: int
    texto: str
    data_insercao: datetime