import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, LargeBinary
from language_crawler.database.base import Base

class ArticleOrm(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, nullable=False)
    article_id = Column(String, nullable=False)
    media_id = Column(String, nullable=False)
    media_name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    is_origin = Column(Boolean, nullable=False)
    original_id = Column(String, nullable=True)
    article_published_at = Column(DateTime(timezone=True), nullable=False)
    latest_scraped_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now(datetime.UTC), nullable=True)

class ArticleContentOrm(Base):
    __tablename__ = 'article_contents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, nullable=False)
    article_id = Column(String, nullable=False)
    media_id = Column(String, nullable=False)
    html = Column(LargeBinary, nullable=False)
    content = Column(String, nullable=True)
    title = Column(String, nullable=True)
    language = Column(String, nullable=False)
    article_published_at = Column(DateTime(timezone=True), nullable=False)
    article_modified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now(datetime.UTC), nullable=True)

class ResearchReport(Base):
    __tablename__ = 'research_reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    target_company = Column(String, nullable=True)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    file_url = Column(String, nullable=False)
    securities_company = Column(String, nullable=False)
    category = Column(String, nullable=True)
    company_id = Column(String, nullable=True)
    report_type = Column(String, nullable=True)
    report_id = Column(String, nullable=True)
    updated_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now(datetime.UTC), nullable=True)

    def __repr__(self):
        return f"<ResearchReport(id={self.id}, title='{self.title}', date='{self.date}', securities_company='{self.securities_company}')>"