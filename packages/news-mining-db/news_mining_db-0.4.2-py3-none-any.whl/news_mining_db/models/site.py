from news_mining_db.models.base_model import Base
from sqlalchemy import Column, Integer, String


class Site(Base):
    __tablename__ = 'site'

    id = Column(Integer, primary_key=True)

    title = Column(String(200))
