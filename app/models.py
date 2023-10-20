from app.database import Base
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship


# class Post(Base):
#     __tablename__ = "posts"
#
#     id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
#     title = Column(String(200), nullable=False)
#     content = Column(String(1000), nullable=False)
#     published = Column(Boolean, server_default=text('TRUE'), nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    #
    # owner = relationship("User")

    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     email = Column(String(100), nullable=False, unique=True)
#     password = Column(String(100), nullable=False)
#     create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#
#
# class Vote(Base):
#     __tablename__ = "votes"
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
#     post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
