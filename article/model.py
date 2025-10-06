#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict
from typing import Optional
from db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, JSON, Boolean, Date, ARRAY
from sqlalchemy.orm import relationship, mapped_column, Mapped


class article_create(BaseModel):
	model_config = ConfigDict(arbitrary_types_allowed=True)
	image: str
	category: list[str]
	title: str
	excerpt: str
	author_id: int
	datePublication: str
	star : int


class article_update(BaseModel):
	model_config = ConfigDict(arbitrary_types_allowed=True)
	image: Optional[str] = None
	category: Optional[list[str]] = None
	title: Optional[str] = None
	excerpt: Optional[str] = None
	author_id: Optional[id] = None
	datePublication: Optional[str] = None
	star : Optional[int] = None


class article(Base):

	__tablename__ = 'article'

	id = Column(Integer, primary_key=True, index=True)

	image= Column(String, nullable= False)
	category= Column(JSON, nullable= False)
	title= Column(String, nullable= False)
	excerpt= Column(String, nullable= False)
	datePublication= Column(String, nullable= False)
	author_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
	author = relationship("UserDB",back_populates="articles")
	star = Column(Integer, nullable=True)
	imageAnnexe = relationship("imageAnnexe", back_populates="article")
 
class imageAnnexe(Base): 
    __tablename__ = "imageAnnexe"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id:Mapped[int] = mapped_column(Integer, ForeignKey("article.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    article = relationship(article, back_populates="imageAnnexe")
    path = Column(String, nullable=True)
    
class imageAnnexeCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    article_id: int
    path: str 