# 算命网站部署指南

## 🚀 部署方案选择

### 方案一：免费云平台部署（推荐新手）✅

**组合：Vercel + Render**

#### 1. 前端部署到 Vercel
```bash
# 1. 安装Vercel CLI
npm install -g vercel

# 2. 进入前端目录
cd frontend

# 3. 登录Vercel
vercel login

# 4. 部署项目
vercel --prod

# 5. 记录生成的域名，例如：https://your-project.vercel.app
```

#### 2. 后端部署到 Render
1. 访问 https://render.com 注册账号
2. 点击 "New +" → "Web Service"
3. 连接您的 GitHub 仓库
4. 配置设置：
   - **Name**: fortune-telling-api
   - **Region**: 选择离您最近的区域
   - **Branch**: main
   - **Root Directory**: backend
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`
5. 添加环境变量：
   ```
   DATABASE_URL=sqlite:///database/fortune.db
   SECRET_KEY=your-very-secure-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
   ```
6. 点击 "Create Web Service"

#### 3. 更新CORS配置
部署完成后，用Render提供的域名替换 `.env.production` 中的 `ALLOWED_ORIGINS`

### 方案二：阿里云/腾讯云部署

#### 1. 购买服务器
- 推荐配置：2核4GB，CentOS 7+/Ubuntu 20+
- 开放端口：22(SSH)、80(HTTP)、443(HTTPS)

#### 2. 服务器环境准备
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Python 3.9+
sudo apt install python3 python3-pip python3-venv -y

# 安装Node.js 16+
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install nodejs -y

# 安装Nginx
sudo apt install nginx -y
```

#### 3. 部署后端
```bash
# 克隆代码
git clone your-repo-url
cd fortune-telling/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务（使用PM2管理）
npm install -g pm2
pm2 start run.py --name "fortune-api" --interpreter python3
pm2 startup
pm2 save
```

#### 4. 部署前端
```bash
# 构建前端
cd ../frontend
npm install
npm run build

# 配置Nginx
sudo nano /etc/nginx/sites-available/fortune
```

Nginx配置示例：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/fortune-telling/frontend/dist;
        try_files $uri $uri/ /index.html;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API代理到后端
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/fortune /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 方案三：Docker部署

创建 `docker-compose.yml`：
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///database/fortune.db
      - SECRET_KEY=your-secret-key
    volumes:
      - ./database:/app/database
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

## 🔧 环境变量配置

### 后端环境变量 (.env)
```
DATABASE_URL=sqlite:///database/fortune.db
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### 前端环境变量 (.env.production)
```
VITE_API_BASE_URL=https://your-backend-domain.com
```

## 📋 部署检查清单

- [ ] 修改生产环境密钥
- [ ] 配置正确的CORS域名
- [ ] 测试API接口连通性
- [ ] 验证用户注册登录功能
- [ ] 测试八字算命核心功能
- [ ] 检查移动端适配
- [ ] 配置SSL证书（HTTPS）

## 🆘 常见问题

### 1. CORS错误
确保后端 `ALLOWED_ORIGINS` 包含前端域名

### 2. API 404错误
检查Nginx代理配置或前端API地址配置

### 3. 数据库连接问题
确认数据库文件路径和权限设置正确

## 🔐 安全建议

1. 使用强密码和密钥
2. 定期备份数据库
3. 配置HTTPS
4. 设置防火墙规则
5. 定期更新依赖包

部署完成后，您将获得一个可公开访问的算命网站链接！