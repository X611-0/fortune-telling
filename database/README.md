# 数据库说明

## 数据库结构

本项目使用 SQLite 数据库，数据库文件位于 `database/fortune.db`

### 数据表说明

1. **users 表** - 用户信息
   - id: 主键
   - username: 用户名（唯一）
   - email: 邮箱（唯一）
   - password_hash: 加密密码
   - created_at: 创建时间

2. **bazi_records 表** - 八字记录
   - id: 主键
   - user_id: 用户ID（外键）
   - year: 年柱
   - month: 月柱
   - day: 日柱
   - hour: 时柱
   - gender: 性别
   - created_at: 创建时间

3. **fortune_records 表** - 算命记录
   - id: 主键
   - user_id: 用户ID（外键）
   - bazi_id: 八字ID（外键）
   - fortune_type: 算命类型
   - result: 算命结果（JSON格式）
   - created_at: 创建时间

## 数据库管理

### 初始化数据库
```bash
cd backend
python manage.py init
```

### 创建数据表
```bash
python manage.py create
```

### 重置数据库（开发环境）
```bash
python manage.py reset
```

### 备份数据库
```bash
python backup_database.py
```

## 数据库连接信息

- **类型**: SQLite
- **文件位置**: `database/fortune.db`
- **连接字符串**: `sqlite:///database/fortune.db`

## 生产环境建议

在生产环境中，建议使用 PostgreSQL 或 MySQL 替代 SQLite：

1. 修改 `.env` 文件中的 `DATABASE_URL`
2. 安装相应的数据库驱动
3. 运行数据库迁移脚本