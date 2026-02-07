from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from pydantic import BaseModel
from fastapi.security import HTTPBearer
from app.core.security import verify_token

router = APIRouter()
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

class UserProfile(BaseModel):
    username: str
    email: str
    created_at: str

@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # current_user 已经是查询到的用户对象，直接返回即可
    return UserProfile(
        username=current_user.username,
        email=current_user.email,
        created_at=current_user.created_at.isoformat()
    )