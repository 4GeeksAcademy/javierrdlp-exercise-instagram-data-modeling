import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)   
    username = Column(String(250), nullable=False, index=True) 
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250))
    email = Column(String(250), nullable=False, unique=True)
    post = relationship('Post', back_populates='user')
    comment = relationship('Comment', back_populates='author')
    users_following = relationship('Follower', foreign_keys ='Follower.user_from_id', back_populates='user_from')
    users_followers = relationship('Follower', foreign_keys ='Follower.user_to_id', back_populates='user_to')

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True) 
    user_from_id = Column(Integer, ForeignKey('user.id'))
    user_to_id = Column(Integer, ForeignKey('user.id'))
    user_from = relationship('User', back_populates='users_following')
    user_to = relationship('User', back_populates='users_followers')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True) 
    comment_text = Column(String(250), nullable=False, )
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship('Post', back_populates='comment')
    author = relationship('User', back_populates='comment')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    media = relationship('Media', back_populates='post')
    user = relationship('User', back_populates='post')
    comment = relationship('Comment', back_populates='post')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum, nullable=False)
    url = Column(String(1000), nullable=False)
    post_id = Column(Integer,  ForeignKey('post.id'), nullable=False)
    post = relationship('Post', back_populates='media') 


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
