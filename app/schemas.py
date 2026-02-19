from pydantic import BaseModel

class LivroBase(BaseModel):
    titulo: str
    autor: str
    ano_publicacao: int

class LivroCreate(LivroBase):
    pass

class LivroUpdate(LivroBase):
    pass

class LivroResponse(LivroBase):
    id: int
    disponivel: bool

    class Config:
        from_attributes = True
