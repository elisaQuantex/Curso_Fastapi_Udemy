from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.core.db import Base

#Esto es opcional para que no me subraye PostORM pero
#deberia funcionar igual sin esto.
if TYPE_CHECKING:
    from .post import PostORM

#Relacion muchos a muchos: Un post puede tener muchos tags(o etiquetas) y un tag puede tener muchos posts.
class TagORM(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30),unique=True, index=True)

    posts: Mapped[List["PostORM"]] = relationship(
        secondary="post_tags",  
        back_populates="tags", 
        lazy="selectin"       #que la busqueda la va a hacer con "selectin"
        )  
