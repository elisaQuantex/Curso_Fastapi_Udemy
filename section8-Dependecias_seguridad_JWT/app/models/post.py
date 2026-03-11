from __future__ import annotations
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Integer, String,Text, DateTime, ForeignKey, UniqueConstraint, Table, Column 
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.core.db import Base

#Esto es opcional para que no me subraye PostORM pero
#deberia funcionar igual sin esto.
if TYPE_CHECKING:
    from .author import AuthorORM
    from .tag import TagORM

post_tags=Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True),
    Column("tags_id", ForeignKey("tags.id",ondelete="CASCADE"),primary_key=True)
)

class PostORM(Base):
    __tablename__="posts"
    __table_args__=(UniqueConstraint("title", name="unique_post_title"),) #le estamos pidiendo que
                                                                          # los titulos sean unicos
    id:Mapped[int]=mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    #relacionamos cada post con su autor:
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("authors.id"))
    author: Mapped[Optional["AuthorORM"]] = relationship(back_populates="posts")
    
    tags: Mapped[List["TagORM"]] = relationship(
        secondary=post_tags,  #la relacion va a ser a traves de la tabla intermedia
        back_populates="posts", #que los tags van a poder acceder a los posts(tablas) por medio de este nombre "posts".
        lazy="selectin",       #que la busqueda la va a hacer con "selectin"
        passive_deletes=True)  #para respetar el ondelete="CASCADE"
    