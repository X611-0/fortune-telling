from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class BaziRecord(Base):
    __tablename__ = "bazi_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    year = Column(String(10), nullable=False)  # 年柱
    month = Column(String(10), nullable=False)  # 月柱
    day = Column(String(10), nullable=False)  # 日柱
    hour = Column(String(10), nullable=False)  # 时柱
    gender = Column(String(10), nullable=False)  # 性别
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    user = relationship("User", back_populates="bazi_records")
    fortune_records = relationship("FortuneRecord", back_populates="bazi")
    love_fortunes = relationship("LoveFortune", back_populates="bazi")  # 新增爱情运势关系
    
    def __repr__(self):
        return f"<BaziRecord(user_id={self.user_id}, bazi='{self.year}{self.month}{self.day}{self.hour}')>"