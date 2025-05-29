from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Date
from sqlalchemy.orm import relationship

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class Settings(db.Model):
    __tablename__ = 'ayarlar'
    id = Column(Integer, primary_key=True)
    site_name = Column(String(255), nullable=False)
    site_description = Column(Text, nullable=False)
    site_keywords = Column(Text, nullable=False)
    site_author = Column(String(255), nullable=False)
    site_footer = Column(Text, nullable=False)
    
    # Anasayfa içeriği
    homepage_title = Column(String(255), nullable=True)
    homepage_subtitle = Column(String(255), nullable=True)
    homepage_content = Column(Text, nullable=True)
    homepage_image = Column(String(255), nullable=True)
    
    # Hakkımızda sayfası içeriği
    about_title = Column(String(255), nullable=True)
    about_content = Column(Text, nullable=True)
    about_image = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f'<Settings {self.site_name}>'
        
# Avukatlar tablosu
class Lawyer(db.Model):
    __tablename__ = 'avukatlar'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    photo = Column(String(255), nullable=True)
    order = Column(Integer, default=0)  # Sıralama için kullanılacak
    
    def __repr__(self):
        return f'<Lawyer {self.name}>'

class User(db.Model):
    __tablename__ = 'kullanici'
    id = Column(Integer, primary_key=True)
    full_name = Column('adsoyad', String(100), nullable=False)
    description = Column('aciklama', Text, nullable=True)
    profile_photo = Column('profilfoto', String(255), nullable=True)
    profession = Column('meslek', String(255), nullable=True)
    phone = Column('telefon', String(25), nullable=True)  # Telefon alan boyutunu arttırdık
    email = Column('mail', String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.full_name}>'

class Service(db.Model):
    __tablename__ = 'hizmetler'
    id = Column(Integer, primary_key=True)
    title = Column('hizmetbaslik', String(255), nullable=False)
    description = Column('hizmetaciklama', Text, nullable=False)
    
    def __repr__(self):
        return f'<Service {self.title}>'

class Expertise(db.Model):
    __tablename__ = 'uzman'
    id = Column(Integer, primary_key=True)
    title = Column('uzmanbaslik', String(255), nullable=False)
    description = Column('uzmanaciklama', Text, nullable=False)
    
    def __repr__(self):
        return f'<Expertise {self.title}>'

class Project(db.Model):
    __tablename__ = 'projeler'
    id = Column(Integer, primary_key=True)
    title = Column('projebaslik', String(255), nullable=False)
    description = Column('projeaciklama', Text, nullable=False)
    category = Column('kategori', String(50), nullable=True)  # Hukuk alanı kategorisi
    image = Column('projegorsel', String(255), nullable=True)  # Fotoğraf zorunlu değil
    date = Column('tarih', DateTime, default=datetime.utcnow)  # Tarih bilgisi
    
    def __repr__(self):
        return f'<Project {self.title}>'

class SocialMedia(db.Model):
    __tablename__ = 'sosyal'
    id = Column(Integer, primary_key=True)
    facebook = Column(String(255), nullable=False)
    instagram = Column(String(255), nullable=False)
    twitter = Column(String(255), nullable=False)
    
    def __repr__(self):
        return f'<SocialMedia {self.id}>'

class Contact(db.Model):
    __tablename__ = 'iletisim'
    id = Column(Integer, primary_key=True)
    full_name = Column('adsoyad', String(255), nullable=False)
    email = Column('mailadresi', String(255), nullable=False)
    subject = Column('konu', String(255), nullable=False)
    message = Column('mesaj', Text, nullable=False)
    ip_address = Column('ip_address', String(45), nullable=True)  # IPv6 için 45 karakter yeterli
    date = Column('tarih', DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contact {self.full_name}>'

class Category(db.Model):
    __tablename__ = 'kategoriler'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with articles
    articles = relationship('Article', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Article(db.Model):
    __tablename__ = 'makaleler'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    image = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey('kategoriler.id'), nullable=True)
    author_id = Column(Integer, ForeignKey('admin.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = Column(Boolean, default=True)
    views = Column(Integer, default=0)
    
    # Relationships
    author = relationship('Admin', backref='articles')
    
    def __repr__(self):
        return f'<Article {self.title}>'