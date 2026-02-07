from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.bazi import BaziRecord
from app.models.user import User
from app.core.security import verify_token
from fastapi.security import HTTPBearer

router = APIRouter(tags=["八字"])
security = HTTPBearer()

def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    """获取当前用户"""
    print("=== 认证中间件开始执行 ===")
    
    # 如果token是None，说明HTTPBearer认证失败
    if token is None:
        print("认证中间件 - HTTPBearer认证失败，token为None")
        raise HTTPException(status_code=401, detail="认证失败：Authorization头格式错误或缺失")
    
    print(f"认证中间件 - 接收到的token对象类型: {type(token)}")
    print(f"认证中间件 - token对象属性: {dir(token) if hasattr(token, '__dir__') else '无属性'}")
    
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
        # 确保返回401状态码而不是403
        raise HTTPException(status_code=401, detail=e.detail)
    except Exception as e:
        print(f"认证中间件 - 发生未知错误: {str(e)}")
        # 对于未知错误，返回500而不是403，以便区分不同类型的错误
        raise HTTPException(status_code=500, detail=f"认证处理错误: {str(e)}")
    finally:
        print("=== 认证中间件执行结束 ===")

# 创建绕过HTTPBearer认证的备用认证函数
def get_current_user_direct(request, db: Session = Depends(get_db)):
    """直接处理Authorization头的认证函数"""
    print("=== 直接认证中间件开始执行 ===")
    
    try:
        # 直接从请求头获取Authorization
        auth_header = request.headers.get("Authorization")
        print(f"直接认证 - Authorization头: {auth_header}")
        
        if not auth_header:
            print("直接认证 - Authorization头缺失")
            raise HTTPException(status_code=401, detail="Authorization头缺失")
        
        # 检查Bearer前缀
        if not auth_header.startswith("Bearer "):
            print("直接认证 - Authorization头格式错误，缺少Bearer前缀")
            raise HTTPException(status_code=401, detail="Authorization头格式错误")
        
        # 提取token
        token_value = auth_header[7:].strip()  # 去掉"Bearer "前缀
        print(f"直接认证 - 提取的token: {token_value[:10]}...(长度:{len(token_value)})")
        
        # 验证token
        username = verify_token(token_value)
        print(f"直接认证 - token验证结果: {'成功' if username else '失败'}")
        
        if not username:
            print("直接认证 - token无效、已过期或格式错误")
            raise HTTPException(status_code=401, detail="无效的令牌")
            
        print(f"直接认证 - 从token中获取用户名: {username}")
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print("直接认证 - 用户不存在")
            raise HTTPException(status_code=404, detail="用户不存在")
        
        print(f"直接认证 - 用户认证成功: {user.username}")
        return user
    except HTTPException as e:
        print(f"直接认证 - HTTP异常: {e.status_code} {e.detail}")
        raise HTTPException(status_code=401, detail=e.detail)
    except Exception as e:
        print(f"直接认证 - 发生未知错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"认证处理错误: {str(e)}")
    finally:
        print("=== 直接认证中间件执行结束 ===")

class BaziCreateRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    gender: str

import time

# 添加测试端点，验证认证机制
@router.get("/test-auth")
async def test_auth(current_user: User = Depends(get_current_user)):
    """测试认证中间件是否正常工作"""
    return {
        "message": "认证测试成功",
        "user": current_user.username,
        "status": "authenticated"
    }

@router.get("/test-no-auth")
async def test_no_auth():
    """测试无需认证的端点"""
    return {
        "message": "无需认证测试成功",
        "status": "public"
    }

@router.get("/test-auth-header")
async def test_auth_header(request: Request):
    """测试Authorization头是否正确传递"""
    print("=== 测试Authorization头 ===")
    auth_header = request.headers.get("Authorization")
    print(f"接收到的Authorization头: {auth_header}")
    
    # 打印所有请求头
    print("所有请求头:")
    for key, value in request.headers.items():
        print(f"  {key}: {value}")
    
    return {
        "message": "Authorization头测试",
        "auth_header_present": auth_header is not None,
        "auth_header_value": auth_header[:20] + "..." if auth_header else "None",
        "auth_header_valid": auth_header and auth_header.startswith("Bearer ")
    }

@router.post("/")
def create_bazi_record(
    request: Request,
    bazi_data: BaziCreateRequest,
    db: Session = Depends(get_db)
):
    # 添加更详细的调试信息
    print("=== 创建八字记录函数开始执行 ===")
    print("=== 请求头详细信息 ===")
    for key, value in request.headers.items():
        print(f"  {key}: {value}")
    
    # 简化认证流程，直接使用Authorization头进行验证
    auth_header = request.headers.get("Authorization")
    print(f"=== 认证调试信息 ===")
    print(f"认证 - Authorization头是否存在: {auth_header is not None}")
    print(f"认证 - Authorization头值: {auth_header}")
    
    if not auth_header:
        print("认证失败 - Authorization头缺失")
        raise HTTPException(status_code=401, detail="认证失败: Authorization头缺失或格式错误")
    
    if not auth_header.startswith("Bearer "):
        print(f"认证失败 - Authorization头格式错误，缺少Bearer前缀")
        print(f"认证失败 - 实际头值: {auth_header}")
        raise HTTPException(status_code=401, detail="认证失败: Authorization头缺失或格式错误")
    
    token_value = auth_header[7:].strip()
    print(f"认证 - 提取的token: {token_value[:20]}...(长度:{len(token_value)})")
    
    # 直接验证token
    username = verify_token(token_value)
    print(f"认证 - token验证结果: {'成功' if username else '失败'}")
    
    if not username:
        print("认证失败 - token无效、已过期或格式错误")
        raise HTTPException(status_code=401, detail="认证失败: 无效的令牌")
    
    # 查找用户
    user = db.query(User).filter(User.username == username).first()
    if not user:
        print(f"认证失败 - 用户不存在: {username}")
        raise HTTPException(status_code=404, detail="用户不存在")
    
    print(f"认证成功 - 当前用户: {user.username}")
    current_user = user
    
    start_time = time.time()
    print(f"创建八字记录 - 用户: {current_user.username}, 开始时间: {start_time}")
    
    try:
        """计算八字"""
        # 这里实现八字计算逻辑
        # 简化版：返回示例数据
        calc_start = time.time()
        bazi_result_data = {
            "year": bazi_data.year,
            "month": bazi_data.month,
            "day": bazi_data.day,
            "hour": bazi_data.hour,
            "gender": bazi_data.gender,
            "bazi_result": "示例八字结果",
            "analysis": "示例分析内容"
        }
        calc_end = time.time()
        print(f"八字计算耗时: {calc_end - calc_start:.4f}秒")
        
        # 保存到数据库
        db_start = time.time()
        bazi_record = BaziRecord(
            user_id=current_user.id,
            year=str(bazi_data.year),  # 转换为字符串
            month=str(bazi_data.month),  # 转换为字符串
            day=str(bazi_data.day),  # 转换为字符串
            hour=str(bazi_data.hour),  # 转换为字符串
            gender=bazi_data.gender
        )
        db.add(bazi_record)
        db.commit()
        db.refresh(bazi_record)
        db_end = time.time()
        print(f"数据库操作耗时: {db_end - db_start:.4f}秒")
        
        end_time = time.time()
        print(f"创建八字记录完成，总耗时: {end_time - start_time:.4f}秒")
        
        return bazi_record
    except Exception as e:
        end_time = time.time()
        print(f"创建八字记录失败，耗时: {end_time - start_time:.4f}秒, 错误: {str(e)}")
        # 添加更详细的错误信息
        print(f"错误类型: {type(e).__name__}")
        print(f"错误详情: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建八字记录失败: {str(e)}")

@router.get("/")
def get_bazi_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"获取八字记录 - 用户: {current_user.username}")
    """获取用户的八字记录"""
    records = db.query(BaziRecord).filter(BaziRecord.user_id == current_user.id).all()
    return records