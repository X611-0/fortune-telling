from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class FortuneCategory(Base):
    """运势分类表"""
    __tablename__ = "fortune_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)  # 分类名称
    description = Column(Text)  # 分类描述
    icon = Column(String(100))  # 分类图标
    color = Column(String(20))  # 分类颜色
    is_active = Column(Boolean, default=True)  # 是否启用
    sort_order = Column(Integer, default=0)  # 排序顺序
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    fortune_records = relationship("FortuneRecord", back_populates="category")
    
    def __repr__(self):
        return f"<FortuneCategory(name='{self.name}', active={self.is_active})>"

class LoveFortune(Base):
    """爱情运势表"""
    __tablename__ = "love_fortunes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bazi_id = Column(Integer, ForeignKey("bazi_records.id"), nullable=False)
    
    # 爱情运势相关字段
    love_level = Column(String(20), nullable=False)  # 爱情运势等级
    romantic_opportunity = Column(String(100))  # 浪漫机会
    compatibility_partner = Column(String(100))  # 最佳配对
    relationship_advice = Column(Text)  # 关系建议
    lucky_meeting_places = Column(String(200))  # 幸运相遇地点
    
    # 详细分析
    emotional_state = Column(String(100))  # 情感状态
    communication_style = Column(String(100))  # 沟通方式
    love_challenges = Column(Text)  # 爱情挑战
    improvement_suggestions = Column(Text)  # 改进建议
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    user = relationship("User", back_populates="love_fortunes")
    bazi = relationship("BaziRecord", back_populates="love_fortunes")
    
    def __repr__(self):
        return f"<LoveFortune(user_id={self.user_id}, level='{self.love_level}')>"

class FortuneRecord(Base):
    __tablename__ = "fortune_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bazi_id = Column(Integer, ForeignKey("bazi_records.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("fortune_categories.id"), nullable=True)  # 关联分类
    fortune_type = Column(String(20), nullable=False)  # 算命类型
    result = Column(Text, nullable=False)  # 算命结果(JSON格式)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    user = relationship("User", back_populates="fortune_records")
    bazi = relationship("BaziRecord", back_populates="fortune_records")
    category = relationship("FortuneCategory", back_populates="fortune_records")  # 新增关系
    
    def __repr__(self):
        return f"<FortuneRecord(user_id={self.user_id}, type='{self.fortune_type}')>"