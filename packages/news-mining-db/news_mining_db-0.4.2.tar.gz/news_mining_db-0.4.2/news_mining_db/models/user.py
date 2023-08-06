from news_mining_db.models.base_model import Base
from sqlalchemy import Column, Integer, String, Boolean
from hashlib import sha256


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    password_hashed = Column(String(16), nullable=False)
    username = Column(String(16), nullable=False, unique=True)
    email = Column(String(32), nullable=False, unique=True)

    is_staff = Column(Boolean, server_default='f', nullable=False)

    @property
    def password(self):
        return self.password_hashed

    @password.setter
    def password(self, value: str):
        self.password_hashed = sha256(bytes(value, 'utf-8')).hexdigest()

    def is_password_correct(self, password: str) -> bool:
        return self.password_hashed == sha256(bytes(password, 'utf-8')).hexdigest()
