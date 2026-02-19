from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Biblioteca")

# Dependência de sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/livros", response_model=schemas.LivroResponse)
def criar(livro: schemas.LivroCreate, db: Session = Depends(get_db)):
    return crud.criar_livro(db, livro)


@app.get("/livros", response_model=list[schemas.LivroResponse])
def listar(db: Session = Depends(get_db)):
    return crud.listar_livros(db)


@app.get("/livros/{livro_id}", response_model=schemas.LivroResponse)
def buscar(livro_id: int, db: Session = Depends(get_db)):
    livro = crud.buscar_livro(db, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@app.put("/livros/{livro_id}", response_model=schemas.LivroResponse)
def atualizar(livro_id: int, livro: schemas.LivroUpdate, db: Session = Depends(get_db)):
    livro_atualizado = crud.atualizar_livro(db, livro_id, livro)
    if not livro_atualizado:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro_atualizado


@app.delete("/livros/{livro_id}")
def deletar(livro_id: int, db: Session = Depends(get_db)):
    livro = crud.deletar_livro(db, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return {"mensagem": "Livro deletado com sucesso"}

@app.post("/livros/{livro_id}/emprestar", response_model=schemas.LivroResponse)
def emprestar(livro_id: int, db: Session = Depends(get_db)):
    resultado = crud.emprestar_livro(db, livro_id)

    if resultado is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    if resultado == "indisponivel":
        raise HTTPException(status_code=400, detail="Livro já está emprestado")

    return resultado


@app.post("/livros/{livro_id}/devolver", response_model=schemas.LivroResponse)
def devolver(livro_id: int, db: Session = Depends(get_db)):
    resultado = crud.devolver_livro(db, livro_id)

    if resultado is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    if resultado == "ja_disponivel":
        raise HTTPException(status_code=400, detail="Livro já está disponível")

    return resultado

