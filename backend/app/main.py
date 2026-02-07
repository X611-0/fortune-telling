from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine
from app.models import user, bazi, fortune
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.bazi import router as bazi_router
from app.routes.fortune import router as fortune_router
from app.routes.admin import router as admin_router
import os

# 确保数据库目录存在
os.makedirs('database', exist_ok=True)

# 创建数据库表
user.Base.metadata.create_all(bind=engine)
bazi.Base.metadata.create_all(bind=engine)
fortune.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="算命网站API", 
    version="1.0.0",
    description="一个基于八字算命的网站后端API"
)

# 配置CORS - 支持生产环境
import os

# 从环境变量获取允许的源，支持多个域名
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000")
allowed_origins_list = [origin.strip() for origin in allowed_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router, prefix="/api/auth", tags=["认证"])
app.include_router(user_router, prefix="/api/user", tags=["用户"])
app.include_router(bazi_router, prefix="/api/bazi", tags=["八字"])
app.include_router(fortune_router, prefix="/api/fortune", tags=["算命"])
app.include_router(admin_router, prefix="/api", tags=["管理"])

@app.get("/")
async def root():
    return {"message": "算命网站API服务运行中", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

@app.on_event("startup")
async def startup_event():
    print("算命网站API服务启动完成！")
    print(f"数据库文件位置: database/fortune.db")