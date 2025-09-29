import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from model.categoria import Categoria


class CategoriaSchema(BaseModel):
    """ Schema para inserção de uma nova Categoria. """
    nome: str = Field(..., example="Transporte")
    ordem: Optional[int] = Field(None, example=1)

class CategoriaPatchSchema(BaseModel):
    """ Schema para inserção de uma nova Categoria. """
    nome: Optional[str] = Field(None, example="Transporte")
    ordem: Optional[int] = Field(None, example=1)

class CategoriaBuscaSchema(BaseModel):
    """ Schema para busca de uma Categoria. """
    nome: Optional[str] = Field(None, example="Transporte")
    id: Optional[uuid.UUID] = Field(None, example=uuid.uuid4())


class CategoriaPathSchema(BaseModel):
    """ Schema para busca de uma Categoria. """
    id: Optional[uuid.UUID] = Field(None, example=uuid.uuid4())


class CategoriaViewSchema(BaseModel):
    id: uuid.UUID
    nome: str   
    ordem: Optional[int] = None


class ListaCategoriasSchema(BaseModel):
    """ Define como uma listagem de categorias será retornada. 
    """
    categorias: List[CategoriaViewSchema]


class CategoriaDelSchema(BaseModel):
    """ Schema para remoção de uma Categoria. """
    id: uuid.UUID = Field(None, example=uuid.uuid4())
    nome: str = Field(None, example="Transporte")
    message: str = Field(None, example="Categoria removida da base")


def apresenta_categoria(categoria: Categoria):
    
    """ Retorna uma representação da categoria seguindo o schema definido em
        CategoriaViewSchema.
    """
    return {
        "id": categoria.id,
        "nome": categoria.nome,
        "ordem": categoria.ordem
    }


def apresenta_categorias(categorias: List[Categoria]):
    """ Retorna uma representação da categoria seguindo o schema definido em
        CategoriaViewSchema.
    """
    result = []
    for categoria in categorias:
        result.append(apresenta_categoria(categoria))

    return {"categorias": result}