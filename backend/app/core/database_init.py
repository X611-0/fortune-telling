import sqlite3
import os
from app.core.config import settings

def init_database():
    """初始化数据库和表结构"""
    # 确保数据库目录存在
    os.makedirs(os.path.dirname('database/'), exist_ok=True)
    
    # 连接SQLite数据库
    conn = sqlite3.connect('database/fortune.db')
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建八字记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bazi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            year VARCHAR(10) NOT NULL,
            month VARCHAR(10) NOT NULL,
            day VARCHAR(10) NOT NULL,
            hour VARCHAR(10) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # 创建运势分类表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fortune_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) UNIQUE NOT NULL,
            description TEXT,
            icon VARCHAR(100),
            color VARCHAR(20),
            is_active BOOLEAN DEFAULT 1,
            sort_order INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建算命记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fortune_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            bazi_id INTEGER NOT NULL,
            category_id INTEGER,
            fortune_type VARCHAR(20) NOT NULL,
            result TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (bazi_id) REFERENCES bazi_records (id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES fortune_categories (id) ON DELETE SET NULL
        )
    ''')
    
    # 创建爱情运势表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS love_fortunes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            bazi_id INTEGER NOT NULL,
            love_level VARCHAR(20) NOT NULL,
            romantic_opportunity VARCHAR(100),
            compatibility_partner VARCHAR(100),
            relationship_advice TEXT,
            lucky_meeting_places VARCHAR(200),
            emotional_state VARCHAR(100),
            communication_style VARCHAR(100),
            love_challenges TEXT,
            improvement_suggestions TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (bazi_id) REFERENCES bazi_records (id) ON DELETE CASCADE
        )
    ''')
    
    # 创建索引以提高查询性能
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_bazi_user_id ON bazi_records(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_fortune_user_id ON fortune_records(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_fortune_bazi_id ON fortune_records(bazi_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_fortune_category_id ON fortune_records(category_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_love_fortune_user_id ON love_fortunes(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_love_fortune_bazi_id ON love_fortunes(bazi_id)')
    
    conn.commit()
    conn.close()
    print("数据库初始化完成！")

if __name__ == "__main__":
    init_database()