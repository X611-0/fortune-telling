from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    bazi_records = relationship("BaziRecord", back_populates="user")
    fortune_records = relationship("FortuneRecord", back_populates="user")
    love_fortunes = relationship("LoveFortune", back_populates="user")  # 新增爱情运势关系
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"