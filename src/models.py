import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
import enum

Base = declarative_base()

# Enum for Post Types
class PostTypeEnum(enum.Enum):
    text = "text"
    photo = "photo"
    gif = "gif"

# User model
class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    # Relationships
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    favorites = relationship('Favorite', back_populates='user')

# Character model
class Character(Base):
    __tablename__ = 'character'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250), nullable=True)
    
    # Relationship
    favorited_by = relationship('Favorite', back_populates='character')

# Planet model
class Planet(Base):
    __tablename__ = 'planet'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250), nullable=True)
    
    # Relationship
    favorited_by = relationship('Favorite', back_populates='planet')

# Favorite model
class Favorite(Base):
    __tablename__ = 'favorite'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    character_id = Column(Integer, ForeignKey('character.id'), nullable=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), nullable=True)

    # Relationships
    user = relationship('User', back_populates='favorites')
    character = relationship('Character', back_populates='favorited_by')
    planet = relationship('Planet', back_populates='favorited_by')

# Post model
class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Enum(PostTypeEnum), nullable=False)
    text_content = Column(Text, nullable=True)  # For text posts
    media_url = Column(String(250), nullable=True)  # For photos or gifs
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

    # Relationships
    user = relationship('User', back_populates='posts')
    category = relationship('Category', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    likes = relationship('Like', back_populates='post')

# Comment model
class Comment(Base):
    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    # Relationships
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')
    likes = relationship('Like', back_populates='comment')

# Category model
class Category(Base):
    __tablename__ = 'category'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # Relationship to posts
    posts = relationship('Post', back_populates='category')

# Like model
class Like(Base):
    __tablename__ = 'like'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=True)
    comment_id = Column(Integer, ForeignKey('comment.id'), nullable=True)

    # Relationships
    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')
    comment = relationship('Comment', back_populates='likes')

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')

