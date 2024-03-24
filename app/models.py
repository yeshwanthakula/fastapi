from .database import Base
from sqlalchemy import Column,String,Integer,Boolean,TIMESTAMP,text,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

#every model is a table

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(Integer , ForeignKey("users.id" , ondelete = "CASCADE") , nullable = False)
    user = relationship("Users")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key = True , nullable = False)
    email = Column(String, unique = True)
    password = Column(String , nullable = False , unique = True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    
class Votes(Base):
    __tablename__ = "votes"
    post_id = Column(Integer ,ForeignKey("posts.id",ondelete = "CASCADE") , primary_key = True )
    user_id = Column(Integer ,ForeignKey("users.id", ondelete = "CASCADE") , primary_key = True )


