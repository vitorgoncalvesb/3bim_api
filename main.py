from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_db
from models import ProdutoDB
from schemas import ProdutoCreate, ProdutoResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GET /produtos/{id}
@app.get('/produtos/{id}', response_model=ProdutoResponse)
def obter_produto(
    id: int,    
    db: Session = Depends(get_db)
):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail='Produto não encontrado'
        )

    return produto


# POST /produtos
@app.post('/produtos', response_model=ProdutoResponse, status_code=201)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db)
):
    novo_produto = ProdutoDB(**produto.model_dump())

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


# DELETE /produtos/{id}
@app.delete('/produtos/{id}', status_code=204)
def remover_produto(
    id: int,
    db: Session = Depends(get_db)
):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail='Produto não encontrado'
        )

    db.delete(produto)
    db.commit()


# PUT /produtos/{id}
@app.put('/produtos/{id}', response_model=ProdutoResponse)
def atualizar_produto(
    id: int,
    dados: ProdutoCreate,
    db: Session = Depends(get_db)
):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail='Produto não encontrado'
        )

    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.quantidade = dados.quantidade

    db.commit()
    db.refresh(produto)

    return produto

@app.get('/produtos', response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(ProdutoDB).all()
    return produtos
