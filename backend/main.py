from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, create_engine, Session, select
from typing import List, Optional
import uvicorn

# 导入模型
from models import Article, User, Collection

# 数据库配置
DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 创建数据库表
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 创建FastAPI应用
app = FastAPI(title="AI项目后端API", version="1.0.0")

# 启动时创建数据库表
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ============== 文章相关接口 ==============
@app.get("/api/articles/", response_model=List[Article])
def read_articles(limit: int = 100, skip: int = 0):
    """获取文章列表"""
    with Session(engine) as session:
        articles = session.exec(select(Article).offset(skip).limit(limit)).all()
    return articles

@app.get("/api/articles/{article_id}", response_model=Article)
def read_article(article_id: int):
    """获取文章详情"""
    with Session(engine) as session:
        article = session.get(Article, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="文章不存在")
    return article

@app.post("/api/articles/", response_model=Article)
def create_article(article: Article):
    """创建新文章"""
    with Session(engine) as session:
        session.add(article)
        session.commit()
        session.refresh(article)
    return article

# ============== 用户相关接口 ==============
@app.post("/api/users/", response_model=User)
def create_user(user: User):
    """创建用户"""
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.username == user.username)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="用户名已存在")
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

# ============== 收藏相关接口 ==============
@app.post("/api/collections/")
def create_collection(collection: Collection):
    """添加收藏"""
    with Session(engine) as session:
        existing_collection = session.exec(
            select(Collection).where(
                Collection.user_id == collection.user_id,
                Collection.article_id == collection.article_id
            )
        ).first()
        if existing_collection:
            raise HTTPException(status_code=400, detail="已收藏该文章")
        
        session.add(collection)
        session.commit()
    return {"message": "收藏成功", "collection_id": collection.id}

# 启动应用
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

