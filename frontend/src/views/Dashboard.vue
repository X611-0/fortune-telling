<template>
  <div class="dashboard-container">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>算命网站</h1>
          <div class="user-info">
            <span>欢迎，{{ authStore.user?.username }}</span>
            <el-button @click="handleLogout" type="text">退出登录</el-button>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <div class="welcome-section">
          <h2>命运探索之旅</h2>
          <p>输入你的八字信息，开始探索你的命运</p>
        </div>
        
        <div class="feature-cards">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-card class="feature-card" @click="$router.push('/bazi')">
                <div class="card-content">
                  <el-icon size="48" color="#409EFF"><User /></el-icon>
                  <h3>输入八字</h3>
                  <p>输入你的生辰八字信息</p>
                </div>
              </el-card>
            </el-col>
            
            <el-col :span="8">
              <el-card class="feature-card" @click="$router.push('/fortune')">
                <div class="card-content">
                  <el-icon size="48" color="#67C23A"><MagicStick /></el-icon>
                  <h3>算命功能</h3>
                  <p>查看各种运势预测</p>
                </div>
              </el-card>
            </el-col>
            
            <el-col :span="8">
              <el-card class="feature-card" @click="$router.push('/records')">
                <div class="card-content">
                  <el-icon size="48" color="#E6A23C"><Document /></el-icon>
                  <h3>个人记录</h3>
                  <p>查看历史算命记录</p>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
        
        <div v-if="userStore.baziRecords.length > 0" class="recent-section">
          <h3>最近的八字记录</h3>
          <el-table :data="userStore.baziRecords.slice(0, 3)" style="width: 100%">
            <el-table-column prop="year" label="年柱" />
            <el-table-column prop="month" label="月柱" />
            <el-table-column prop="day" label="日柱" />
            <el-table-column prop="hour" label="时柱" />
            <el-table-column prop="gender" label="性别" />
            <el-table-column prop="created_at" label="创建时间" />
          </el-table>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { User, MagicStick, Document } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const authStore = useAuthStore()
const userStore = useUserStore()

onMounted(async () => {
  await userStore.getBaziRecords()
})

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    authStore.logout()
    router.push('/login')
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
  padding: 40px 0;
}

.welcome-section h2 {
  color: #333;
  margin-bottom: 10px;
}

.welcome-section p {
  color: #666;
  font-size: 16px;
}

.feature-cards {
  margin-bottom: 40px;
}

.feature-card {
  cursor: pointer;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.card-content {
  text-align: center;
  padding: 20px;
}

.card-content h3 {
  margin: 15px 0 10px;
  color: #333;
}

.card-content p {
  color: #666;
}

.recent-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.recent-section h3 {
  margin-bottom: 20px;
  color: #333;
}
</style>