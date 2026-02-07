from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from ..core.database import get_db
from ..models.user import User
from ..models.bazi import BaziRecord
from ..models.fortune import FortuneRecord, LoveFortune, FortuneCategory

router = APIRouter(prefix="/admin", tags=["admin"])

# Pydantic模型定义
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class BaziRecordCreate(BaseModel):
    user_id: int
    year: str
    month: str
    day: str
    hour: str
    gender: str

class BaziRecordUpdate(BaseModel):
    year: Optional[str] = None
    month: Optional[str] = None
    day: Optional[str] = None
    hour: Optional[str] = None
    gender: Optional[str] = None

class FortuneRecordCreate(BaseModel):
    user_id: int
    bazi_id: int
    category_id: int
    result: str

class FortuneRecordUpdate(BaseModel):
    category_id: Optional[int] = None
    result: Optional[str] = None

class LoveFortuneCreate(BaseModel):
    user_id: int
    bazi_id: int
    love_level: str
    romantic_opportunity: str
    compatibility_partner: str

class LoveFortuneUpdate(BaseModel):
    love_level: Optional[str] = None
    romantic_opportunity: Optional[str] = None
    compatibility_partner: Optional[str] = None

class FortuneCategoryCreate(BaseModel):
    name: str
    description: str
    icon: str
    color: str
    is_active: bool = True

class FortuneCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None

# 用户管理API
@router.get("/users", response_model=List[dict])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username, "email": u.email, "created_at": u.created_at.isoformat()} for u in users]

@router.post("/users")
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    user = User(username=user_data.username, email=user_data.email)
    user.set_password(user_data.password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message": "用户创建成功", "user_id": user.id}

@router.put("/users/{user_id}")
async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user_data.username:
        user.username = user_data.username
    if user_data.email:
        user.email = user_data.email
    
    db.commit()
    return {"message": "用户更新成功"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db.delete(user)
    db.commit()
    return {"message": "用户删除成功"}

# 八字记录管理API
@router.get("/bazi-records", response_model=List[dict])
async def get_bazi_records(db: Session = Depends(get_db)):
    records = db.query(BaziRecord).all()
    return [{"id": r.id, "user_id": r.user_id, "year": r.year, "month": r.month, 
             "day": r.day, "hour": r.hour, "gender": r.gender, "created_at": r.created_at.isoformat()} for r in records]

@router.post("/bazi-records")
async def create_bazi_record(record_data: BaziRecordCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == record_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    record = BaziRecord(
        user_id=record_data.user_id,
        year=record_data.year,
        month=record_data.month,
        day=record_data.day,
        hour=record_data.hour,
        gender=record_data.gender
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return {"message": "八字记录创建成功", "record_id": record.id}

@router.put("/bazi-records/{record_id}")
async def update_bazi_record(record_id: int, record_data: BaziRecordUpdate, db: Session = Depends(get_db)):
    record = db.query(BaziRecord).filter(BaziRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="八字记录不存在")
    
    if record_data.year:
        record.year = record_data.year
    if record_data.month:
        record.month = record_data.month
    if record_data.day:
        record.day = record_data.day
    if record_data.hour:
        record.hour = record_data.hour
    if record_data.gender:
        record.gender = record_data.gender
    
    db.commit()
    return {"message": "八字记录更新成功"}

@router.delete("/bazi-records/{record_id}")
async def delete_bazi_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(BaziRecord).filter(BaziRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="八字记录不存在")
    
    db.delete(record)
    db.commit()
    return {"message": "八字记录删除成功"}

# 算命记录管理API
@router.get("/fortune-records", response_model=List[dict])
async def get_fortune_records(db: Session = Depends(get_db)):
    records = db.query(FortuneRecord).all()
    return [{"id": r.id, "user_id": r.user_id, "bazi_id": r.bazi_id, 
             "category_id": r.category_id, "result": r.result, "created_at": r.created_at.isoformat()} for r in records]

@router.post("/fortune-records")
async def create_fortune_record(record_data: FortuneRecordCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == record_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    bazi_record = db.query(BaziRecord).filter(BaziRecord.id == record_data.bazi_id).first()
    if not bazi_record:
        raise HTTPException(status_code=404, detail="八字记录不存在")
    
    category = db.query(FortuneCategory).filter(FortuneCategory.id == record_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    record = FortuneRecord(
        user_id=record_data.user_id,
        bazi_id=record_data.bazi_id,
        category_id=record_data.category_id,
        result=record_data.result
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return {"message": "算命记录创建成功", "record_id": record.id}

@router.put("/fortune-records/{record_id}")
async def update_fortune_record(record_id: int, record_data: FortuneRecordUpdate, db: Session = Depends(get_db)):
    record = db.query(FortuneRecord).filter(FortuneRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="算命记录不存在")
    
    if record_data.category_id:
        category = db.query(FortuneCategory).filter(FortuneCategory.id == record_data.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="分类不存在")
        record.category_id = record_data.category_id
    
    if record_data.result:
        record.result = record_data.result
    
    db.commit()
    return {"message": "算命记录更新成功"}

@router.delete("/fortune-records/{record_id}")
async def delete_fortune_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(FortuneRecord).filter(FortuneRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="算命记录不存在")
    
    db.delete(record)
    db.commit()
    return {"message": "算命记录删除成功"}

# 爱情运势管理API
@router.get("/love-fortunes", response_model=List[dict])
async def get_love_fortunes(db: Session = Depends(get_db)):
    fortunes = db.query(LoveFortune).all()
    return [{"id": f.id, "user_id": f.user_id, "bazi_id": f.bazi_id, 
             "love_level": f.love_level, "romantic_opportunity": f.romantic_opportunity,
             "compatibility_partner": f.compatibility_partner, "created_at": f.created_at.isoformat()} for f in fortunes]

@router.post("/love-fortunes")
async def create_love_fortune(fortune_data: LoveFortuneCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == fortune_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    bazi_record = db.query(BaziRecord).filter(BaziRecord.id == fortune_data.bazi_id).first()
    if not bazi_record:
        raise HTTPException(status_code=404, detail="八字记录不存在")
    
    fortune = LoveFortune(
        user_id=fortune_data.user_id,
        bazi_id=fortune_data.bazi_id,
        love_level=fortune_data.love_level,
        romantic_opportunity=fortune_data.romantic_opportunity,
        compatibility_partner=fortune_data.compatibility_partner
    )
    
    db.add(fortune)
    db.commit()
    db.refresh(fortune)
    
    return {"message": "爱情运势创建成功", "fortune_id": fortune.id}

@router.put("/love-fortunes/{fortune_id}")
async def update_love_fortune(fortune_id: int, fortune_data: LoveFortuneUpdate, db: Session = Depends(get_db)):
    fortune = db.query(LoveFortune).filter(LoveFortune.id == fortune_id).first()
    if not fortune:
        raise HTTPException(status_code=404, detail="爱情运势不存在")
    
    if fortune_data.love_level:
        fortune.love_level = fortune_data.love_level
    if fortune_data.romantic_opportunity:
        fortune.romantic_opportunity = fortune_data.romantic_opportunity
    if fortune_data.compatibility_partner:
        fortune.compatibility_partner = fortune_data.compatibility_partner
    
    db.commit()
    return {"message": "爱情运势更新成功"}

@router.delete("/love-fortunes/{fortune_id}")
async def delete_love_fortune(fortune_id: int, db: Session = Depends(get_db)):
    fortune = db.query(LoveFortune).filter(LoveFortune.id == fortune_id).first()
    if not fortune:
        raise HTTPException(status_code=404, detail="爱情运势不存在")
    
    db.delete(fortune)
    db.commit()
    return {"message": "爱情运势删除成功"}

# 运势分类管理API
@router.get("/fortune-categories", response_model=List[dict])
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(FortuneCategory).all()
    return [{"id": c.id, "name": c.name, "description": c.description, 
             "icon": c.icon, "color": c.color, "is_active": c.is_active, 
             "created_at": c.created_at.isoformat()} for c in categories]

@router.post("/fortune-categories")
async def create_fortune_category(category_data: FortuneCategoryCreate, db: Session = Depends(get_db)):
    category = FortuneCategory(
        name=category_data.name,
        description=category_data.description,
        icon=category_data.icon,
        color=category_data.color,
        is_active=category_data.is_active
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return {"message": "运势分类创建成功", "category_id": category.id}

@router.put("/fortune-categories/{category_id}")
async def update_fortune_category(category_id: int, category_data: FortuneCategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(FortuneCategory).filter(FortuneCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="运势分类不存在")
    
    if category_data.name:
        category.name = category_data.name
    if category_data.description:
        category.description = category_data.description
    if category_data.icon:
        category.icon = category_data.icon
    if category_data.color:
        category.color = category_data.color
    if category_data.is_active is not None:
        category.is_active = category_data.is_active
    
    db.commit()
    return {"message": "运势分类更新成功"}

@router.delete("/fortune-categories/{category_id}")
async def delete_fortune_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(FortuneCategory).filter(FortuneCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="运势分类不存在")
    
    db.delete(category)
    db.commit()
    return {"message": "运势分类删除成功"}