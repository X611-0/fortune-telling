#!/usr/bin/env python3
"""
数据库备份脚本
"""
import sqlite3
import shutil
import datetime
import os

def backup_database():
    """备份数据库文件"""
    source_db = 'database/fortune.db'
    
    if not os.path.exists(source_db):
        print("数据库文件不存在，无法备份")
        return
    
    # 创建备份目录
    backup_dir = 'database/backups'
    os.makedirs(backup_dir, exist_ok=True)
    
    # 生成备份文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f'{backup_dir}/fortune_backup_{timestamp}.db'
    
    # 复制数据库文件
    shutil.copy2(source_db, backup_file)
    print(f"数据库备份完成: {backup_file}")

def list_backups():
    """列出所有备份文件"""
    backup_dir = 'database/backups'
    if not os.path.exists(backup_dir):
        print("备份目录不存在")
        return
    
    backups = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
    if not backups:
        print("没有找到备份文件")
        return
    
    print("可用的备份文件:")
    for backup in sorted(backups):
        print(f"  - {backup}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_backups()
    else:
        backup_database()