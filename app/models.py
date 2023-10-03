from database import Base
from sqlalchemy import Column, String, Integer, DateTime, Boolean

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(String(1000), nullable=False)
    published = Column(Boolean, default=True)


