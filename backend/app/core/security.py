from datetime import datetime, timedelta
import jwt
import hashlib
import hmac
from app.core.config import settings

def verify_password(plain_password, hashed_password):
    # 检查是否是我们的哈希格式
    if hashed_password.startswith("sha256:"):
        # 使用HMAC-SHA256验证
        salt = settings.SECRET_KEY.encode('utf-8')
        password_bytes = plain_password.encode('utf-8')
        
        expected_hash = hmac.new(salt, password_bytes, hashlib.sha256).hexdigest()
        return f"sha256:{expected_hash}" == hashed_password
    else:
        # 如果是旧格式，尝试兼容处理
        try:
            # 如果可能，尝试使用passlib验证
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
            return pwd_context.verify(plain_password, hashed_password)
        except:
            return False

def get_password_hash(password):
    # 确保密码是字符串类型
    if not isinstance(password, str):
        password = str(password)
    
    # 使用HMAC-SHA256作为主要方案
    salt = settings.SECRET_KEY.encode('utf-8')
    password_bytes = password.encode('utf-8')
    
    # 使用HMAC-SHA256进行哈希
    hashed = hmac.new(salt, password_bytes, hashlib.sha256).hexdigest()
    return f"sha256:{hashed}"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        # 输入验证
        if not token or not isinstance(token, str):
            print("Token为空或不是字符串")
            return None
        
        print(f"验证token - 输入token长度: {len(token)} 字符")
        # 检查是否有Bearer前缀，如果有则移除
        if token.startswith("Bearer "):
            print("Token包含Bearer前缀，正在移除")
            token = token[7:].strip()
        
        # 检查token格式
        if not token:
            print("Token移除前缀后为空")
            return None
            
        # 检查token结构（JWT应有三段）
        if '.' not in token:
            print("Token缺少分隔符，不是有效的JWT格式")
            return None
            
        token_parts = token.split('.')
        if len(token_parts) != 3:
            print(f"Token段数错误，应为3段，实际为{len(token_parts)}段")
            return None
            
        print(f"验证token: {token[:20]}...(长度:{len(token)})")
        # 使用密钥解码token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print("Token解码成功")
        
        # 验证payload中的必要字段
        if not isinstance(payload, dict):
            print("Token payload不是有效的字典格式")
            return None
            
        # 检查payload中是否包含必要的字段
        if 'sub' not in payload:
            print("验证token - 失败: payload中缺少'sub'字段")
            return None
            
        username: str = payload.get("sub")
        if username is None:
            print("Token中没有找到用户名(sub)")
            return None
            
        if not isinstance(username, str) or not username.strip():
            print("Token中的用户名字段无效")
            return None
            
        print(f"验证token - 成功，用户: {username}")
        return username
    except jwt.ExpiredSignatureError:
        print("Token已过期")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Token格式无效: {str(e)}")
        return None
    except Exception as e:
        import traceback
        print(f"验证token - 失败: 发生未知错误, {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return None