from fastapi import FastAPI
from app.core.db import Base, engine
from dotenv import load_dotenv
from app.api.v1.posts.router import router as post_router #un alias
from app.api.v1.auth.router import router as auth_router

load_dotenv()
                 
def create_app() -> FastAPI: 
    app = FastAPI(title="Mini Blog")
    Base.metadata.create_all(bind=engine) # dev. Crea las tablas en caso de que no exista.
                                      #esto es para desarrollo. EN produccion vamos a 
                                      #usar migraciones.
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(post_router)
    return app

app = create_app()





    