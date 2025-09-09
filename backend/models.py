from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

# 文章表
class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str
    summary: Optional[str] = None
    tags: str = "[]"  # 存储JSON格式标签列表
    create_time: datetime = Field(default=datetime.now())
    update_time: datetime = Field(default=datetime.now(), sa_column_kwargs={"onupdate": datetime.now()})

# 用户表（人设管理）
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str  # 实际项目应加密存储
    role: str = "user"  # user/admin
    profile: str = "{}"  # 存储人设JSON

# 收藏表
class Collection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    article_id: int = Field(foreign_key="article.id")
    collection_type: str = "favorite"  # favorite/plan

