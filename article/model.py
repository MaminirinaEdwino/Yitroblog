#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict
from typing import Optional
from db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, JSON, Boolean, Date
from sqlalchemy.orm import relationship, mapped_column, Mapped


class article_create(BaseModel):
	model_config = ConfigDict(arbitrary_types_allowed=True)
	image: str
	category: str
	title: str
	excerpt: str
	author_id: int
	datePublication: str


class article_update(BaseModel):
	model_config = ConfigDict(arbitrary_types_allowed=True)
	image: Optional[str] = None
	category: Optional[str] = None
	title: Optional[str] = None
	excerpt: Optional[str] = None
	author_id: Optional[id] = None
	datePublication: Optional[str] = None


class article(Base):

	__tablename__ = 'article'

	id = Column(Integer, primary_key=True, index=True)

	image= Column(String, nullable= False)
	category= Column(String, nullable= False)
	title= Column(String, nullable= False)
	excerpt= Column(String, nullable= False)
	# author= Column(String, nullable= False)
	datePublication= Column(String, nullable= False)
	author_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
	author = relationship("UserDB",back_populates="articles")