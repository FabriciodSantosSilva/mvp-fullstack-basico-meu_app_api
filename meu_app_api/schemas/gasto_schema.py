import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Importa os schemas de visualização para aninhamento
from schemas import *
from schemas import NotaGastoViewSchema


class GastoSchema(BaseModel):
    """ Schema para inserção de um novo Gasto. """
    descricao: str
    valor: float
    # O Gasto requer o ID da Categoria
    categoria_id: uuid.UUID
    data_gasto: Optional[datetime] = None

class GastoPatchSchema(BaseModel):
    """ Schema para atualização de um novo Gasto. """
    descricao: Optional[str] = Field(None, example="Emergência falta de gás")
    valor: Optional[float] = Field(None, example=120.0)
    categoria_id: Optional[uuid.UUID] = Field(None, example=uuid.uuid4())
    data_gasto: Optional[datetime] = Field(None, example="2025-09-28T14:48:00")

class GastoBuscaSchema(BaseModel):
    """ Schema para busca de Gasto por ID. """
    id: uuid.UUID

class GastoPathSchema(BaseModel):
    """ Schema para busca de uma Gasto. """
    id: Optional[uuid.UUID] = Field(None, example=uuid.uuid4())


class GastoViewSchema(BaseModel):
    """ Schema para retorno/visualização de um Gasto completo. """
    id: uuid.UUID
    descricao: str
    valor: float
    data_insercao: datetime
    data_gasto: datetime
    # Aninhamento do objeto Categoria
    categoria_obj: CategoriaViewSchema
    # Aninhamento da lista de Notas/Comentários
    # O nome do campo deve ser 'notas', conforme o relacionamento em model/gasto.py
    notas: List[NotaGastoViewSchema] = []


class ListaGastosViewSchema(BaseModel):
    """ Schema para retorno de uma lista de Gastos. """
    gastos: List[GastoViewSchema]


class GastoDelSchema(BaseModel):
    """ Schema para mensagem de sucesso ao deletar um Gasto. """
    mesage: str
    descricao: str



def apresenta_gasto(gasto):
    def formatar_data_br(dt):
        if not dt:
            return None
        from datetime import datetime, timedelta
        if isinstance(dt, str):
            try:
                dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
            except Exception:
                return dt
        dt_br = dt - timedelta(hours=3)
        return dt_br.strftime('%Y-%m-%d %H:%M:%S')

    return {
        "id": gasto.id,
        "descricao": gasto.descricao,
        "valor": gasto.valor,
        "data_insercao": formatar_data_br(gasto.data_insercao),
        "data_gasto": formatar_data_br(gasto.data_gasto),
        "categoria_obj": apresenta_categoria(gasto.categoria_obj) if getattr(gasto, "categoria_obj", None) else None,
        "notas": getattr(gasto, "notas", [])
    }

def apresenta_gastos(gastos):
    """Retorna uma lista de gastos serializados."""
    result = []
    for gasto in gastos:
        result.append(apresenta_gasto(gasto))
    return {"gastos": result}