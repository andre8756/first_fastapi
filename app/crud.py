from sqlalchemy.orm import Session
from . import models, schemas

def criar_livro(db: Session, livro: schemas.LivroCreate):
    db_livro = models.Livro(**livro.model_dump())
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro


def listar_livros(db: Session):
    return db.query(models.Livro).all()


def buscar_livro(db: Session, livro_id: int):
    return db.query(models.Livro).filter(models.Livro.id == livro_id).first()


def atualizar_livro(db: Session, livro_id: int, livro: schemas.LivroUpdate):
    db_livro = buscar_livro(db, livro_id)

    if db_livro:
        for key, value in livro.model_dump().items():
            setattr(db_livro, key, value)

        db.commit()
        db.refresh(db_livro)

    return db_livro


def deletar_livro(db: Session, livro_id: int):
    db_livro = buscar_livro(db, livro_id)

    if db_livro:
        db.delete(db_livro)
        db.commit()

    return db_livro


def emprestar_livro(db: Session, livro_id: int):
    livro = buscar_livro(db, livro_id)

    if not livro:
        return None

    if not livro.disponivel:
        return "indisponivel"

    livro.disponivel = False
    db.commit()
    db.refresh(livro)

    return livro


def devolver_livro(db: Session, livro_id: int):
    livro = buscar_livro(db, livro_id)

    if not livro:
        return None

    if livro.disponivel:
        return "ja_disponivel"

    livro.disponivel = True
    db.commit()
    db.refresh(livro)

    return livro

