from fastapi import FastAPI, Query, Body, HTTPException, Path
from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, List, Union, Literal
from math import ceil

app = FastAPI(title="Mini Blog")

BLOG_POST= [
    {"id":1, "title":"Hola desde FastAPI", "content":"Mi primer post con FastAPI", "tags": [ {"name":"Python"},{"name":"fastapi"}]},
    {"id":2, "title":"Mi segundo post con FastAPI", "content":"Mi segundo post con FastAPI blablabla"},
    {"id":3, "title":"Django vs FastAPI", "content":"FastAPI es más rápido por x razones"},
    {"id":4, "title":"Hola desde FastAPI", "content":"Mi primer post con FastAPI"},
    {"id":5, "title":"Mi segundo post con FastAPI", "content":"Mi segundo post con FastAPI blablabla","tags": [ {"name":"Python"},{"name":"fastapi"}]},
    {"id":6, "title":"Django vs FastAPI", "content":"FastAPI es más rápido por x razones"},
    {"id":7, "title":"Hola desde FastAPI", "content":"Mi primer post con FastAPI"},
    {"id":8, "title":"Mi segundo post con FastAPI", "content":"Mi segundo post con FastAPI blablabla"},
    {"id":9, "title":"Django vs FastAPI", "content":"FastAPI es más rápido por x razones"},
    {"id":10, "title":"Hola desde FastAPI", "content":"Mi primer post con FastAPI"},
    {"id":11, "title":"Mi segundo post con FastAPI", "content":"Mi segundo post con FastAPI blablabla"},
    {"id":12, "title":"Django vs FastAPI", "content":"FastAPI es más rápido por x razones"}
]

class Tag(BaseModel):
    name: str= Field(..., min_length=2, max_length=30, description="Nombre de la etiqueta")
    
class Autor(BaseModel):
    name: str= Field(..., min_length=2, max_length=30, description="Autor del post")
    email: EmailStr
    
class PostBase(BaseModel):
    title: str
    #content:Optional[str]="Contenido no disponible" # Este es el valor por defecto.
    content: str
    tags: Optional[List[Tag]] =Field(default_factory=list) #[], Si ponemos una lista asi [] es como una lista
                                                          #de python y python es muy flexible y eso puede dar
                                                         #problemas.
    autor: Optional[Autor] = None
    
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
    autor: Optional[Autor]=None
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
    
class PostSummary(BaseModel):
    id:int
    title: str
    
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

@app.get("/")
def home():
    return {'message':'Bienvenidos a Mini Blog por Ricardo'}

#query parameters
@app.get("/posts", response_model=PaginatedPost)
def list_posts(
    text:Optional[str] = Query(
    default=None,
    deprecated=True, 
    description="Parámetro obsoleto. Usa 'query o search' en su lugar",
    ),
    query:Optional[str] = Query(
    default=None, 
    description="Texto para buscar por título",
    alias="search",
    min_length=3,
    max_length=50,
    pattern=r"^[\w\sáéíóúÁÉÍÓÚüÜ-]+$"
    ),
    per_page: int = Query(
       10, ge=1, le=50,
       description="Número de resultados (1-50)" 
    ),# paginación cuando el endpoint devuelve muchos resultados
    #es necesario para no realentizar todo.
    page:int = Query(
        1, ge=1,
        description="Número de pagina (>=1)."
    ), # desde que nro vamos a empezar
    order_by: Literal["id","title"] = Query(
        "id", description="Campo de orden"
    ),
    direction: Literal["asc","desc"]=Query(
        "asc", description="Direccion de orden"
    )
    ):  #le paso un parámetro que tiene que ser
                                   #de tipo string o ninguno.
    results = BLOG_POST
    query = query or text
    if query:
        '''
        results=[]
        for post in BLOG_POST:
            if query.lower() in post["title"].lower():
                results.append(post)
        Esto mismo se puede hacer con una list comprehension:
        '''
        results= [post for post in results if query.lower() in post["title"].lower()]
        # return {"data": results, "query":query}  --> esto ya no hace falta pore ahora agregé response_model.
    #return {"data": BLOG_POST}  --> acá igual, al haber agregado response_model
    total = len(results)
    total_pages=ceil(total/per_page) if total > 0 else 0  
    if total_pages==0:
        current_page=1
    else:
        current_page=min(page, total_pages)
    results = sorted(results, key=lambda post: post[order_by], reverse=(direction=="desc")) #lambda es una funcion que se usa solo acá.
    if total_pages==0:
        items=[]
    else:
        start=(current_page-1)*per_page
        items = results[start:start+per_page] #desde donde empieza y  hasta donde llega  
                                         #dice que devuelva el atributo order_by del objeto post.
    has_prev=current_page>1
    has_next=current_page<total_pages  if total_pages>0 else False
    return PaginatedPost(page= current_page, 
                         per_page=per_page,
                         total=total, 
                         total_pages= total_pages, 
                         has_prev=has_prev, 
                         has_next=has_next, 
                         order_by=order_by, 
                         direction=direction,
                         search=query, 
                         items=items)

@app.get("/posts/by-tags", response_model=List[PostPublic])
def filter_by_tags(
    tags: List[str]=Query(
        ...,
        min_legth=2,
        description="Una o más etiquetas. Ejemplo: ?tags=python&tags=fastapi"
    )
):
    tags_lower=[tag.lower() for tag in tags]
    return [
        post for post in BLOG_POST if any( tag["name"].lower() in tags_lower for tag in post.get("tags",[]))
    ]

#path parameters + query parameter
@app.get("/posts/{post_id}", response_model=Union[PostPublic, PostSummary], response_description="Post encontrado") #Evala y se fija es de tipo PostPubli y sino, se fija si es de tipo PostSummary
def get_post(post_id:int= Path(
    ...,
    ge=1, #mayor o igual
    title = "Id del post",
    description="identificador entero del post. Debe ser mayot a 1.",
    example=1
    ), include_content:bool = Query(default=True, description="Incluye contenido o no") ):
    for post in BLOG_POST:
        if post["id"] == post_id:
            if not include_content:
                return {"id": post["id"], "title":post["title"]}
            # return {"data":post} --> lo cambio porqe ya tengo response_model
            return post
    return HTTPException(status_code=404, detail="POst no encontrado")

#post
@app.post("/posts", response_model=PostPublic, response_description="POst creado (ok)")
def create_post(post: PostCreate): 
    
    #Comento esto porque al pasarle PostCreate ya le digo que valide los datos como estan en esa clase.
    #if "title" not in post or "content" not in post:
    #    return {"error": "Title y Content son requeridos."}
    #if not str(post["title"]).strip(): #paso a string el title y le saco los espacios.
    #    return {"error": "Title no puede estar vacío"}
    
    new_id =(BLOG_POST[-1]["id"]+1) if BLOG_POST else 1
    new_post={"id": new_id,"title":post.title,
              "content":post.content, 
              "tags": [tag.model_dump() for tag in post.tags],
              "autor":post.autor.model_dump() if post.autor else None}  #ahora son atributos de clase, no: post['title']
    BLOG_POST.append(new_post)
    return new_post

@app.put("/posts/{post_id}", response_model= PostPublic, response_description="Post actualizado", response_model_exclude_none=True) #ecluye los none
def update_post(post_id:int, data: PostUpdate):
    for post in BLOG_POST:
        if post["id"]== post_id:
            playload=  data.model_dump(exclude_unset=True) #personalizo la data (objeto) y la convierto en diccionario 
                                                           #con model_dump().
                                                           #exclude_unset=True-->excluir los valores que no le 
                                                           # enviemos.  
                                                           # Entonces, si yo mando {"title": "ricardo"}, me devuelve:
                                                           #{"title":"ricardo"} y no: {"title":"ricardo", "content": None}  
            if "title" in playload: post["title"] = playload["title"]
            if "Content" in playload: post["Content"] = playload["Content"]
            return post
    raise HTTPException(status_code=404, detail="Post no encontrado")

@app.delete("/posts/{post_id}", status_code=204) #Como no quiero devolver nada, solo pongo return y status code 204.
def delete_post(post_id:int):
    for index, post in enumerate(BLOG_POST):
        if post["id"] == post_id:
            BLOG_POST.pop(index)
            return
    raise HTTPException(status_code=404,detail="Post no encontrado")