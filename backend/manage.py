#!/usr/bin/env python3
"""
数据库管理脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database_init import init_database
from app.core.database import engine
from app.models import user, bazi, fortune

def create_tables():
    """创建所有数据表"""
    print("正在创建数据库表...")
    user.Base.metadata.create_all(bind=engine)
    bazi.Base.metadata.create_all(bind=engine)
    fortune.Base.metadata.create_all(bind=engine)
    print("数据库表创建完成！")

def drop_tables():
    """删除所有数据表（开发环境使用）"""
    confirm = input("确定要删除所有数据表吗？这将清除所有数据！(y/N): ")
    if confirm.lower() == 'y':
        print("正在删除数据库表...")
        user.Base.metadata.drop_all(bind=engine)
        bazi.Base.metadata.drop_all(bind=engine)
        fortune.Base.metadata.drop_all(bind=engine)
        print("数据库表删除完成！")
    else:
        print("操作已取消")

def reset_database():
    """重置数据库（删除并重新创建）"""
    drop_tables()
    create_tables()

def show_help():
    """显示帮助信息"""
    print("""
数据库管理命令：
    init     - 初始化数据库
    create   - 创建所有表
    drop     - 删除所有表
    reset    - 重置数据库
    help     - 显示此帮助信息
    """)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        init_database()
        create_tables()
    elif command == "create":
        create_tables()
    elif command == "drop":
        drop_tables()
    elif command == "reset":
        reset_database()
    elif command == "help":
        show_help()
    else:
        print(f"未知命令: {command}")
        show_help()