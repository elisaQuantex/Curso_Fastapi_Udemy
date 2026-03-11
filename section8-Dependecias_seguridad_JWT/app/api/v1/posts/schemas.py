from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict
from typing import Optional, List, Literal

class Tag(BaseModel):
    name: str= Field(..., min_length=2, max_length=30, description="Nombre de la etiqueta")
    model_config = ConfigDict(from_attributes=True) #Esta validacion tambien va aceptar ORMs.
                                                    #Va aceptar objetos del ORM. Si no lo ponemos
                                                    #solo va a aceptar diccionarios.
    
class Autor(BaseModel):
    name: str= Field(..., min_length=2, max_length=30, description="Autor del post")
    email: EmailStr
    model_config = ConfigDict(from_attributes=True) 
    
class PostBase(BaseModel):
    title: str
    #content:Optional[str]="Contenido no disponible" # Este es el valor por defecto.
    content: str
    tags: Optional[List[Tag]] =Field(default_factory=list) #[], Si ponemos una lista asi [] es como una lista
                                                          #de python y python es muy flexible y eso puede dar
                                                         #problemas.
    author: Optional[Autor] = None
    model_config = ConfigDict(from_attributes=True) 
    
class PostCreate(BaseModel):
    title: str=Field(
        ..., #Le digo que el campo title tiene que ser obligatorio (elipsis).
        min_length=3,
        max_length=100,
        description="Título del post (mínimo 3 caracteres, máximo 100)",
        examples=["Mi primer post con FastAPI"]
    )
    content: Optional[str]=Field(
        default="Contenido no disponible",
        min_length=10,
        description="Contenido del post (mínimo 10 caracteres)",
        examples=["Este es un contenido válido porque tiene 10 caracteres o más"]
    )
    tags: List[Tag]=Field(default_factory=list) 
    author: Optional[Autor]=None
    @field_validator("title") #Decorador. Ya utilicé validaciones automáticas (como el tipo que hay
                              #que pasar para el titulo). Validaciones automaticas 
                              #utilizando Field. Y esto (field_validator) me sirve para 
                              # validaciones que ya no vienen por defecto como en Field, 
                              # sino que es bien personal de mi aplicación.
    @classmethod
    def not_allowed_title(cls,value:str) -> str:
        if "spam" in value.lower():
            raise ValueError("El título no puede contener la palabra: 'spam'")
        return value
    
class PostUpdate(BaseModel):
    title: Optional[str]=Field(None, min_length=3, max_length=100)
    content: Optional[str] = None #No va a tener un valor por defecto.

class PostPublic(PostBase): #hererdo de PostBase los atribtos titulo y content
    id: int
    model_config = ConfigDict(from_attributes=True) # model config. Me va ayudar a que podamos enviar los
                                                    #datos de la clase hacia el orm. De esta forma Pydantic entiende
                                                    #que está recibiendo un objeto ORM de sqlalchemy y lo
                                                    #convierte a json
    
class PostSummary(BaseModel):
    id:int
    title: str
    model_config=ConfigDict(from_attributes=True)
    
class PaginatedPost(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    order_by: Literal["id","title"]
    direction: Literal["asc","desc"]
    search: Optional[str]=None
    items: List[PostPublic]