from news_mining_db.models.base_model import Base
from sqlalchemy import Column, Integer, String, Boolean


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    password = Column(String(16), nullable=False)
    username = Column(String(16), nullable=False, unique=True)
    email = Column(String(32), nullable=False, unique=True)

    is_staff = Column(Boolean, server_default='f', nullable=False)
