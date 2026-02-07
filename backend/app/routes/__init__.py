# 路由模块初始化
from .auth import router as auth_router
from .user import router as user_router
from .bazi import router as bazi_router
from .fortune import router as fortune_router

__all__ = ["auth_router", "user_router", "bazi_router", "fortune_router"]