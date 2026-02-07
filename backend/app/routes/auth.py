from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

# 测试端点，用来验证请求和认证头
@router.get("/test-auth")
async def test_auth(request: dict):
    """测试端点，用于验证请求头和认证信息"""
    from fastapi import Request
    
    # 由于FastAPI的限制，我们需要修改函数参数
    # 这里先返回基本信息，稍后会在正确的实现中获取请求头
    return {
        "message": "测试端点正常工作",
        "timestamp": "现在时间",
        "status": "success"
    }

# 正确的测试端点实现
@router.get("/test-token")
async def test_token(request: Request):
    """测试Authorization头是否正确传递"""
    auth_header = request.headers.get("Authorization")
    print(f"测试端点接收到的Authorization头: {auth_header}")
    
    # 测试HTTPBearer认证
    try:
        from fastapi.security import HTTPBearer
        security = HTTPBearer()
        token = await security(request)
        print(f"HTTPBearer认证成功 - token: {token.credentials[:20]}...")
        
        # 测试verify_token函数
        from app.core.security import verify_token
        username = verify_token(token.credentials)
        print(f"Token验证结果: {username}")
        
        return {
            "message": "认证测试成功",
            "auth_header_present": auth_header is not None,
            "auth_header_start": auth_header[:30] + "..." if auth_header else "无",
            "bearer_auth_success": True,
            "token_validation": "成功" if username else "失败",
            "username": username
        }
    except Exception as e:
        print(f"认证测试失败: {str(e)}")
        return {
            "message": "认证测试失败",
            "auth_header_present": auth_header is not None,
            "auth_header_start": auth_header[:30] + "..." if auth_header else "无",
            "bearer_auth_success": False,
            "error": str(e)
        }
security = HTTPBearer()

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=dict)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # 检查用户是否已存在
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    # 创建新用户
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message": "注册成功", "user_id": user.id}

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}