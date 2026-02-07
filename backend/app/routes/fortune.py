from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.models.fortune import FortuneRecord, FortuneCategory, LoveFortune
from app.models.user import User
from app.models.bazi import BaziRecord
from app.core.security import verify_token
from fastapi.security import HTTPBearer
import json

router = APIRouter(tags=["运势"])
security = HTTPBearer()

def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    """获取当前用户"""
    try:
        # 检查token格式
        if not hasattr(token, 'credentials'):
            print("认证中间件 - token格式错误，缺少credentials属性")
            raise HTTPException(status_code=401, detail="token格式错误")
        
        token_value = token.credentials
        print(f"认证中间件 - 收到token: {token_value[:10]}...(长度:{len(token_value)})")  # 只打印部分token
        
        # 直接调用verify_token，它现在会自己处理Bearer前缀
        username = verify_token(token_value)
        print(f"认证中间件 - token验证结果: {'成功' if username else '失败'}")
        
        if not username:
            print("认证中间件 - token无效、已过期或格式错误")
            raise HTTPException(status_code=401, detail="无效的令牌")
            
        print(f"认证中间件 - 从token中获取用户名: {username}")
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print("认证中间件 - 用户不存在")
            raise HTTPException(status_code=404, detail="用户不存在")
        
        print(f"认证中间件 - 用户认证成功: {user.username}")
        return user
    except HTTPException as e:
        # 重新抛出已有的HTTPException，保持原始错误信息
        print(f"认证中间件 - HTTP异常: {e.status_code} {e.detail}")
        raise
    except Exception as e:
        print(f"认证中间件 - 发生未知错误: {str(e)}")
        # 对于未知错误，返回500而不是403，以便区分不同类型的错误
        raise HTTPException(status_code=500, detail=f"认证处理错误: {str(e)}")

class FortuneCalculateRequest(BaseModel):
    bazi_id: int
    fortune_type: str

class FortuneResponse(BaseModel):
    id: int
    user_id: int
    bazi_id: int
    fortune_type: str
    result: str
    created_at: str

class FortuneCategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    color: str
    is_active: bool
    sort_order: int

class LoveFortuneRequest(BaseModel):
    bazi_id: int

class LoveFortuneResponse(BaseModel):
    id: int
    user_id: int
    bazi_id: int
    love_level: str
    romantic_opportunity: str
    compatibility_partner: str
    relationship_advice: str
    lucky_meeting_places: str
    emotional_state: str
    communication_style: str
    love_challenges: str
    improvement_suggestions: str
    created_at: str

@router.post("/")
def calculate_fortune(
    request: FortuneCalculateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """计算运势"""
    # 这里实现运势计算逻辑
    # 简化版：返回示例数据
    fortune_data = {
        "fortune_type": request.fortune_type,
        "result": f"{request.fortune_type}运势分析结果"
    }
    
    # 保存到数据库 - 明确设置category_id为None
    fortune_record = FortuneRecord(
        user_id=current_user.id,
        bazi_id=request.bazi_id,
        category_id=None,  # 明确设置为None
        fortune_type=request.fortune_type,
        result=fortune_data["result"]
    )
    db.add(fortune_record)
    db.commit()
    db.refresh(fortune_record)
    
    return {"message": "运势计算成功", "data": fortune_data}

@router.get("/categories")
def get_fortune_categories(db: Session = Depends(get_db)):
    """获取运势分类列表"""
    # 这里应该返回运势分类，但当前没有FortuneCategory模型
    # 暂时返回示例数据
    categories = [
        {"id": 1, "name": "爱情运势", "description": "分析个人感情运势"},
        {"id": 2, "name": "事业运势", "description": "分析事业发展运势"},
        {"id": 3, "name": "财运", "description": "分析财富积累运势"}
    ]
    return {"categories": categories}

@router.post("/love")
def calculate_love_fortune(
    request: LoveFortuneRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """计算爱情运势"""
    # 验证八字记录是否存在且属于当前用户
    bazi_record = db.query(BaziRecord).filter(
        BaziRecord.id == request.bazi_id,
        BaziRecord.user_id == current_user.id
    ).first()
    
    if not bazi_record:
        raise HTTPException(status_code=404, detail="八字记录不存在")
    
    # 基于八字计算爱情运势（这里使用模拟算法）
    love_data = calculate_love_fortune_from_bazi(bazi_record)
    
    # 创建爱情运势记录
    love_fortune = LoveFortune(
        user_id=current_user.id,
        bazi_id=request.bazi_id,
        **love_data
    )
    db.add(love_fortune)
    db.commit()
    db.refresh(love_fortune)
    
    return {"message": "爱情运势计算成功", "data": love_fortune}

@router.get("/love/records")
def get_love_fortune_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的爱情运势记录"""
    records = db.query(FortuneRecord).filter(
        FortuneRecord.user_id == current_user.id,
        FortuneRecord.fortune_type == "love"
    ).all()
    return {"records": records}

@router.get("/records")
def get_fortune_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的运势记录"""
    records = db.query(FortuneRecord).filter(FortuneRecord.user_id == current_user.id).all()
    return {"records": records}

def calculate_love_fortune_from_bazi(bazi_record):
    """基于八字计算爱情运势（模拟算法）"""
    # 这里使用简化的模拟算法
    # 实际应用中应该使用更复杂的八字算法
    
    # 基于日柱和性别判断爱情运势
    day_pillar = bazi_record.day
    gender = bazi_record.gender
    
    # 简化的爱情运势计算逻辑
    if "甲" in day_pillar or "乙" in day_pillar:
        love_level = "极佳"
        romantic_opportunity = "近期会有浪漫邂逅"
        compatibility_partner = "属虎、属马的人"
    elif "丙" in day_pillar or "丁" in day_pillar:
        love_level = "良好"
        romantic_opportunity = "朋友介绍或社交活动"
        compatibility_partner = "属兔、属羊的人"
    elif "戊" in day_pillar or "己" in day_pillar:
        love_level = "中等"
        romantic_opportunity = "需要主动出击"
        compatibility_partner = "属龙、属狗的人"
    elif "庚" in day_pillar or "辛" in day_pillar:
        love_level = "一般"
        romantic_opportunity = "工作或学习场合"
        compatibility_partner = "属蛇、属鸡的人"
    else:
        love_level = "需要努力"
        romantic_opportunity = "耐心等待缘分"
        compatibility_partner = "属鼠、属猴的人"
    
    # 根据性别调整建议
    if gender == "男":
        relationship_advice = "主动表达情感，展现真诚"
        emotional_state = "热情主动"
    else:
        relationship_advice = "保持优雅，等待合适时机"
        emotional_state = "温柔细腻"
    
    return {
        "love_level": love_level,
        "romantic_opportunity": romantic_opportunity,
        "compatibility_partner": compatibility_partner,
        "relationship_advice": relationship_advice,
        "lucky_meeting_places": "公园、咖啡厅、图书馆",
        "emotional_state": emotional_state,
        "communication_style": "直接坦诚",
        "love_challenges": "需要克服害羞心理",
        "improvement_suggestions": "多参加社交活动，提升自信"
    }