#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional
from db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, JSON, Boolean, Date
	
class article_create(BaseModel):

	image: str
	category: str
	title: str
	excerpt: str
	author: str
	datePublication: str


class article_update(BaseModel):

	image: Optional[str] = None
	category: Optional[str] = None
	title: Optional[str] = None
	excerpt: Optional[str] = None
	author: Optional[str] = None
	datePublication: Optional[str] = None


class article(Base):

	__tablename__ = 'article'

	id = Column(Integer, primary_key=True, index=True)

	image= Column(String, nullable= False)
	category= Column(String, nullable= False)
	title= Column(String, nullable= False)
	excerpt= Column(String, nullable= False)
	author= Column(String, nullable= False)
	datePublication= Column(String, nullable= False)
