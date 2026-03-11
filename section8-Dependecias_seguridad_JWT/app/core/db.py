
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

#Todo hasta app=FastAPI es la configuración para conectarnos a una base de datos.
DATABASE_URL = "postgresql+psycopg://ravasi:Pruebas123@localhost:5432/blogfastapi"
#DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db") #en sqlite le puedo
                                                                #poner el nombre que quiera.
engine_kwargs={}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"]={"check_same_thread":False}

engine=create_engine(DATABASE_URL,echo=True, future=True,**engine_kwargs)  #creamos la conexion
SessionLocal=sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session) #cramos una sesion

class Base(DeclarativeBase):
    pass

#funcion para poder crear la sesion
#cada vez que yo entre a los endpoint me cree la sesion
#y la cierre cuando salga.
# No pongo return (sino yield), porque return termina ahi y yo necesito
#que vuelva a finally. yield es una expresión generadora. Yield es como un return con pausa.
#le entregamos la db a quien necesita, esperamos a que la termine de usar y volvemos
# y close (la cerramos).
# Dependencia: Es una funcion que se puede inyectar automaticamente en los endpoints. 
def get_db():
    db=SessionLocal() #inicializamos una sesión
    try:
        yield db
    finally:
        db.close()