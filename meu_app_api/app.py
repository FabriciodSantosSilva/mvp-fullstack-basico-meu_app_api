from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

#from schemas.categoria import apresenta_categoria, apresenta_categorias
from sqlalchemy.exc import IntegrityError

#from model import Session, categoria, Comentario
from model import Session, Categoria, Gasto
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="ControleDeGastos API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
categoria_tag = Tag(name="Categoria", description="Adição, visualização e remoção de categorias à base")
gasto_tag = Tag(name="Gastos", description="Adição, visualização e remoção de gastos à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# Rotas para Categorias
@app.post('/categorias', tags=[categoria_tag],
          responses={"200": CategoriaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_categoria(form: CategoriaSchema):
    """Adiciona um novo categoria à base de dados

    Retorna uma representação dos categorias e comentários associados.
    """
    categoria = Categoria(
        nome=form.nome,
        ordem=form.ordem
    )
    logger.debug(f"Adicionando categoria de nome: '{categoria.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando categoria
        session.add(categoria)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado categoria de nome: '{categoria.nome}'")
        return apresenta_categoria(categoria), 201

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "categoria de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar categoria '{categoria.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar categoria '{categoria.nome}', {error_msg}")
        return {"message": error_msg}, 400
    

@app.get('/categorias', tags=[categoria_tag],
         responses={"200": ListaCategoriasSchema, "404": ErrorSchema})
def get_categorias():
    """Faz a busca por todos as Categorias cadastradas

    Retorna uma representação da listagem de categorias.
    """
    logger.debug(f"Coletando categorias")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    categorias = session.query(Categoria).all()

    if not categorias:
        # se não há categorias cadastrados
        return {"categorias": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(categorias))
        # retorna a representação de categoria
        print(categorias)
        return apresenta_categorias(categorias), 200
    
@app.get('/categorias/<uuid:id>', tags=[categoria_tag],  
         responses={"200": CategoriaViewSchema, "404": ErrorSchema})
def get_categoria(path: CategoriaPathSchema):
    """Faz a busca por categorias cadastradas filtrando pelo ID.

    Retorna uma representação da listagem de categorias.
    """
    # criando conexão com a base
    session = Session()
    
    # Construindo a query dinamicamente com base nos parâmetros fornecidos
    query_base = session.query(Categoria)
    
    
    if not path.id:
        error_msg = "ID da categoria é obrigatório para busca."
        logger.warning(f"Erro ao buscar categoria, {error_msg}")
        return {"message": error_msg}, 422
    
    query_base = query_base.filter(Categoria.id == path.id)
    
    categoria = query_base.first()

    if not categoria:
        # se o produto não foi encontrado
        search_term = path.id
        error_msg = "Categoria não encontrada na base :/"
        logger.warning(f"Erro ao buscar categoria '{search_term}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Categoria econtrado: '{categoria.nome}'")
        # retorna a representação de Categoria
        return apresenta_categoria(categoria), 200
    

@app.delete('/categoria/<uuid:id>', tags=[categoria_tag],
            responses={"200": CategoriaDelSchema, "404": ErrorSchema, "400": ErrorSchema})
def del_categoria(path: CategoriaPathSchema):
    """Remove uma categoria da base de dados.

    Retorna uma mensagem de confirmação da remoção.
    """
    try:
        # criando conexão com a base
        session = Session()
        categoria = session.query(Categoria).filter(Categoria.id == path.id).first()
        if not categoria:
            # se o categoria não foi encontrado
            error_msg = "Categoria não encontrada na base :/"
            logger.warning(f"Erro ao deletar categoria #'{path.id}', {error_msg}")
            return {"message": error_msg}, 404
        
        nome_deletado = categoria.nome
        id_deletado = categoria.id
        
        # fazendo a remoção
        session.delete(categoria)
        session.commit()
        logger.debug(f"Categoria '{nome_deletado}' (ID: {id_deletado}) removida")
        return {
            "id": id_deletado,
            "nome": nome_deletado,
            "mensagem": "Categoria removida da base"
        }, 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível remover o item :/"
        logger.warning(f"Erro ao remover categoria '{categoria.nome}', {error_msg}")
        return {"message": error_msg}, 400
    

@app.put('/categorias/<uuid:id>', tags=[categoria_tag],  
         responses={"200": CategoriaViewSchema, "404": ErrorSchema})
def update_categoria(path: CategoriaPathSchema, form: CategoriaSchema):
    """Atualiza uma categoria
    """
    # criando conexão com a base
    session = Session()
    
    # Construindo a query dinamicamente com base nos parâmetros fornecidos
    query_base = session.query(Categoria)
    
    
    if not path.id:
        error_msg = "ID da categoria é obrigatório para busca."
        logger.warning(f"Erro ao buscar categoria, {error_msg}")
        return {"message": error_msg}, 422
    
    query_base = query_base.filter(Categoria.id == path.id)
    
    categoria = query_base.first()

    if not categoria:
        # se o produto não foi encontrado
        search_term = path.id
        error_msg = "Categoria não encontrada na base :/"
        logger.warning(f"Erro ao buscar categoria '{search_term}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Categoria econtrado: '{categoria.nome}'")
        categoria.nome = form.nome
        categoria.ordem = form.ordem
        # retorna a representação de Categoria

        try:
            session.commit()
            return apresenta_categoria(categoria), 200
        except IntegrityError as e:
            session.rollback()
            # Relança a exceção para ser tratada na camada de Service/HTTP
            raise IntegrityError("Tentativa de atualizar para um nome de categoria duplicado.", {}, {}) from e

@app.patch('/categorias/<uuid:id>', tags=[categoria_tag],  
         responses={"200": CategoriaViewSchema, "404": ErrorSchema})
def partial_update_categoria(path: CategoriaPathSchema, form: CategoriaPatchSchema):
    """Atualiza parcialmente uma categoria
    """
    # criando conexão com a base
    session = Session()
    
    # Construindo a query dinamicamente com base nos parâmetros fornecidos
    query_base = session.query(Categoria)
    
    
    if not path.id:
        error_msg = "ID da categoria é obrigatório para busca."
        logger.warning(f"Erro ao buscar categoria, {error_msg}")
        return {"message": error_msg}, 422
    
    query_base = query_base.filter(Categoria.id == path.id)
    
    categoria = query_base.first()

    if not categoria:
        # se o produto não foi encontrado
        search_term = path.id
        error_msg = "Categoria não encontrada na base :/"
        logger.warning(f"Erro ao buscar categoria '{search_term}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Categoria econtrado: '{categoria.nome}'")
        if form.nome is not None and form.nome != "":
            categoria.nome = form.nome
        if form.ordem is not None and form.ordem != "":
            categoria.ordem = form.ordem
        # retorna a representação de Categoria

        try:
            session.commit()
            return apresenta_categoria(categoria), 200
        except IntegrityError as e:
            session.rollback()
            # Relança a exceção para ser tratada na camada de Service/HTTP
            raise IntegrityError("Tentativa de atualizar para um nome de categoria duplicado.", {}, {}) from e

# Rotas para Gastos
@app.post('/gastos', tags=[gasto_tag],
          responses={"200": GastoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_gasto(form: GastoSchema):
    """Adiciona um novo gasto à base de dados

    Retorna uma representação dos gastos e comentários associados.
    """
    gasto = Gasto(
        descricao=form.descricao,
        valor=form.valor,
        categoria_id=form.categoria_id,
        data_gasto=form.data_gasto
    )
    logger.debug(f"Adicionando gasto de nome: '{gasto}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando gasto
        session.add(gasto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado gasto de nome: '{gasto}'")
        return apresenta_gasto(gasto), 201

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "gasto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar gasto '{gasto}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar gasto '{gasto}', {error_msg}")
        return {"message": error_msg}, 400
    

@app.get('/gastos', tags=[gasto_tag],
         responses={"200": ListaGastosViewSchema, "404": ErrorSchema})
def get_gastos():
    """Faz a busca por todos as Gastos cadastradas

    Retorna uma representação da listagem de gastos.
    """
    logger.debug(f"Coletando gastos")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    gastos = session.query(Gasto).all()

    if not gastos:
        # se não há gastos cadastrados
        return {"gastos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(gastos))
        # retorna a representação de gasto
        print(gastos)
        return apresenta_gastos(gastos), 200
    
@app.get('/gastos/<uuid:id>', tags=[gasto_tag],  
         responses={"200": GastoViewSchema, "404": ErrorSchema})
def get_gasto(path: GastoPathSchema):
    """Faz a busca por gastos cadastradas filtrando pelo ID.

    Retorna uma representação da listagem de gastos.
    """
    # criando conexão com a base
    session = Session()
    
    # Construindo a query dinamicamente com base nos parâmetros fornecidos
    query_base = session.query(Gasto)
    
    
    if not path.id:
        error_msg = "ID da gasto é obrigatório para busca."
        logger.warning(f"Erro ao buscar gasto, {error_msg}")
        return {"message": error_msg}, 422
    
    query_base = query_base.filter(Gasto.id == path.id)
    
    gasto = query_base.first()

    if not gasto:
        # se o produto não foi encontrado
        search_term = path.id
        error_msg = "Gasto não encontrada na base :/"
        logger.warning(f"Erro ao buscar gasto '{search_term}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Gasto econtrado: '{gasto}'")
        # retorna a representação de Gasto
        return apresenta_gasto(gasto), 200
    

@app.delete('/gasto/<uuid:id>', tags=[gasto_tag],
            responses={"200": GastoDelSchema, "404": ErrorSchema, "400": ErrorSchema})
def del_gasto(path: GastoPathSchema):
    """Remove uma gasto da base de dados.

    Retorna uma mensagem de confirmação da remoção.
    """
    try:
        # criando conexão com a base
        session = Session()
        gasto = session.query(Gasto).filter(Gasto.id == path.id).first()
        if not gasto:
            # se o gasto não foi encontrado
            error_msg = "Gasto não encontrada na base :/"
            logger.warning(f"Erro ao deletar gasto #'{path.id}', {error_msg}")
            return {"message": error_msg}, 404
        
        nome_deletado = gasto
        id_deletado = gasto.id
        
        # fazendo a remoção
        session.delete(gasto)
        session.commit()
        logger.debug(f"Gasto '{nome_deletado}' (ID: {id_deletado}) removida")
        return {
            "id": id_deletado,
            "nome": nome_deletado,
            "mensagem": "Gasto removida da base"
        }, 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível remover o item :/"
        logger.warning(f"Erro ao remover gasto '{gasto}', {error_msg}")
        return {"message": error_msg}, 400
    

@app.put('/gastos/<uuid:id>', tags=[gasto_tag],  
         responses={"200": GastoViewSchema, "404": ErrorSchema})
def update_gasto(path: GastoPathSchema, form: GastoSchema):
    """Atualiza uma gasto
    """
    # criando conexão com a base
    session = Session()
    
    # Construindo a query dinamicamente com base nos parâmetros fornecidos
    query_base = session.query(Gasto)
    
    
    if not path.id:
        error_msg = "ID da gasto é obrigatório para busca."
        logger.warning(f"Erro ao buscar gasto, {error_msg}")
        return {"message": error_msg}, 422
    
    query_base = query_base.filter(Gasto.id == path.id)
    
    gasto = query_base.first()

    if not gasto:
        # se o produto não foi encontrado
        search_term = path.id
        error_msg = "Gasto não encontrada na base :/"
        logger.warning(f"Erro ao buscar gasto '{search_term}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Gasto econtrado: '{gasto}'")
        gasto.descricao = form.descricao
        gasto.valor = form.valor
        gasto.categoria_id = form.categoria_id
        gasto.data_gasto = form.data_gasto
        # retorna a representação de Gasto

        try:
            session.commit()
            return apresenta_gasto(gasto), 200
        except IntegrityError as e:
            session.rollback()
            # Relança a exceção para ser tratada na camada de Service/HTTP
            raise IntegrityError("Tentativa de atualizar para um nome de gasto duplicado.", {}, {}) from e

@app.patch('/gastos/<uuid:id>', tags=[gasto_tag],  
         responses={"200": GastoViewSchema, "404": ErrorSchema})
def partial_update_gasto(path: GastoPathSchema, form: GastoPatchSchema):
    """Atualiza parcialmente uma gasto
    """
    # criando conexão com a base
    session = Session()
    
    # Construindo a query dinamicamente com base nos parâmetros fornecidos
    query_base = session.query(Gasto)
    
    
    if not path.id:
        error_msg = "ID da gasto é obrigatório para busca."
        logger.warning(f"Erro ao buscar gasto, {error_msg}")
        return {"message": error_msg}, 422
    
    query_base = query_base.filter(Gasto.id == path.id)
    
    gasto = query_base.first()

    if not gasto:
        # se o produto não foi encontrado
        search_term = path.id
        error_msg = "Gasto não encontrada na base :/"
        logger.warning(f"Erro ao buscar gasto '{search_term}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Gasto econtrado: '{gasto}'")
        if form.descricao is not None and form.descricao != "":
            gasto.descricao = form.descricao
        if form.categoria_id is not None and form.categoria_id != "":
            gasto.categoria_id = form.categoria_id
        if form.data_gasto is not None and form.data_gasto != "":
            gasto.data_gasto = form.data_gasto
        if form.valor is not None and form.valor != "":
            gasto.valor = form.valor
            
        # retorna a representação de Gasto

        try:
            session.commit()
            return apresenta_gasto(gasto), 200
        except IntegrityError as e:
            session.rollback()
            # Relança a exceção para ser tratada na camada de Service/HTTP
            raise IntegrityError("Tentativa de atualizar para um nome de gasto duplicado.", {}, {}) from e