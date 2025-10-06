from fastapi import APIRouter,Depends, HTTPException, UploadFile, File, Form 
from security import *
from article.model import article, article_create, article_update, imageAnnexeCreate, imageAnnexe 
from db import get_db
from requests import Session
import shutil
from user import UserDB
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from typing import List

article_router = APIRouter(prefix="/article", tags=['article'])


@article_router.get("/")
async def get_all_article(db: Session = Depends(get_db)):
	# db_article = db.query(article).all()	
	query = select(article)
	query = query.options(joinedload(article.author))
	
	# query = query.join(UserDB)
	db_article = db.execute(query)
	res = []
	for art in db_article.scalars().all():
	    print(art)
	    res.append(
						{
          		"id": art.id,
				"image": art.image,
				"title":  art.title,
				"datePublication": art.datePublication,
				"category": art.category,
				"excerpt": art.excerpt,
				"author_id": art.author_id,
				"star":art.star,
				"author": {
				"id": art.author.id,
				"username":art.author.username,
				"full_name": art.author.full_name,
				"email":art.author.email
				}
			}
		)
    
	return res

@article_router.get("/{id}")
async def get_article_by_id(id: int, db: Session = Depends(get_db)):
    query = select(article).filter(article.id == id)
    query = query.options(joinedload(article.author))
    # db_article = db.query(article).filter(article.id == id).first()
    db_article = db.execute(query)
    
    if not db_article:
        raise HTTPException(status_code=404, detail="article not found")
    # db_article.scalars().all()[0]
    art = db_article.scalars().all()[0]
    return {
          		"id": art.id,
				"image": art.image,
				"title":  art.title,
				"datePublication": art.datePublication,
				"category": list(art.category),
				"excerpt": art.excerpt,
				"star":art.star,
				"author": {
				"id": art.author.id,
				"username":art.author.username,
				"full_name": art.author.full_name,
				"email":art.author.email
				}
			}

# @article_router.post("/")
# async def create_article(article_post: article_create, db: Session = Depends(get_db)):
# 	db_article = article(**article_post.model_dump())
# 	db.add(db_article)
# 	db.commit()
# 	db.refresh(db_article)
# 	return db_article

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)

imageAnnexeRouter = APIRouter(prefix="/image/annexe", tags=['image annexe'])


@imageAnnexeRouter.post("/", dependencies=[Depends(get_current_active_admin)])
async def postImage(image: List[UploadFile] = File(...), article_id: int = Form(...), db: Session = Depends(get_db)):
    
    for file in image: 
        img = imageAnnexeCreate(
			article_id=article_id,
			path=file.filename.replace(' ','')
		)
        db_image = imageAnnexe(**img.model_dump())
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        filepath = os.path.join(UPLOAD_DIR, file.filename.replace(' ', ''))
        with open(filepath, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
     
	
    return {
		"files":[ file.filename for file in image]
	}
    
@imageAnnexeRouter.delete("/{id}", dependencies=[Depends(get_current_active_admin)])
async def deleteImage(id: int, db: Session = Depends(get_db)):
    db_image = db.query(imageAnnexe).filter(imageAnnexe.id == id).first()
    if not db_image:
       raise HTTPException(status_code=404, detail="article not found")
    
    db.delete(db_image)
    db.commit()
    return {"message": "article deleted successfully"}
    
@imageAnnexeRouter.get("/article/{id}")
async def getAllImageAnnexe(id: int, db: Session = Depends(get_db)):
    img =  db.query(imageAnnexe).filter(imageAnnexe.article_id == id)
    res = []
    for i in img:
        res.append(i)
    return res

@article_router.post('/', dependencies=[Depends(get_current_active_admin)])
async def postarticle(
    image: UploadFile = File(...),  
    category: str = Form(...),
    title: str = Form(...),
    excerpt: str = Form(...),
    author_id: int = Form(...),
    date: datetime = Form(...),
    star: int = Form(...),
    db: Session = Depends(get_db)):
    filepath = os.path.join(UPLOAD_DIR, image.filename)
    print(category[0])
    category = str(category)
    category = category.split(",")
    art = article_create(
		image=image.filename,
		category=category,
		title= title,
		excerpt=excerpt,
		datePublication= str(date),
		author_id=author_id,
		star=star
	)
    db_article = article(**art.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    with open(filepath, "wb") as buffer: shutil.copyfileobj(image.file, buffer)
	
    return {
		"image": image.filename,
		"category": category,
		"title": title,
		"excerpt": excerpt,
		"author_id": author_id,
		"date": date,
		"star": star
	}
     
@article_router.put("/{id}", dependencies=[Depends(get_current_active_admin)])
async def update_article(id: int, article_put: article_update, db: Session = Depends(get_db)):
	db_article = db.query(article).filter(article.id == id).first()
	if not db_article:
		raise HTTPException(status_code=404, detail="article not found")
	for key, value in article_put.model_dump().items():
		if value is not None:
			setattr(db_article, key, value)
	db.commit()
	db.refresh(db_article)
	return db_article

@article_router.delete("/{id}", dependencies=[Depends(get_current_active_admin)])
async def delete_article(id: int, db: Session = Depends(get_db)):
	db_article = db.query(article).filter(article.id == id).first()
	if not article:
		raise HTTPException(status_code=404, detail="article not found")
	db.delete(db_article)
	db.commit()
	return {"message": "article deleted successfully"}

# @article_router.get("/{image}")
# async def get_article_by_image(image: str, db: Session = Depends(get_db)):
# 	db_article = db.query(article).filter(article.image == image).all()	
# 	if not db_article:
# 		raise HTTPException(status_code=404, detail="article not found")
# 	return db_article

# @article_router.get("/{category}")
# async def get_article_by_category(category: str, db: Session = Depends(get_db)):
# 	db_article = db.query(article).filter(article.category == category).all()	
# 	if not db_article:
# 		raise HTTPException(status_code=404, detail="article not found")
# 	return db_article

# @article_router.get("/{title}")
# async def get_article_by_title(title: str, db: Session = Depends(get_db)):
# 	db_article = db.query(article).filter(article.title == title).all()	
# 	if not db_article:
# 		raise HTTPException(status_code=404, detail="article not found")
# 	return db_article

# @article_router.get("/{excerpt}")
# async def get_article_by_excerpt(excerpt: str, db: Session = Depends(get_db)):
# 	db_article = db.query(article).filter(article.excerpt == excerpt).all()	
# 	if not db_article:
# 		raise HTTPException(status_code=404, detail="article not found")
# 	return db_article

# @article_router.get("/{author}")
# async def get_article_by_author(author: str, db: Session = Depends(get_db)):
# 	db_article = db.query(article).filter(article.author == author).all()	
# 	if not db_article:
# 		raise HTTPException(status_code=404, detail="article not found")
# 	return db_article

# @article_router.get("/{date}")
# async def get_article_by_date(date: str, db: Session = Depends(get_db)):
# 	db_article = db.query(article).filter(article.date == date).all()	
# 	if not db_article:
# 		raise HTTPException(status_code=404, detail="article not found")
# 	return db_article
