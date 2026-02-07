<template>
  <div class="records-container">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>个人记录</h1>
          <div class="header-actions">
            <el-button @click="$router.push('/')">返回首页</el-button>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <!-- 八字记录 -->
        <el-card class="bazi-records-card">
          <template #header>
            <div class="card-header">
              <span>八字记录</span>
              <el-button type="primary" @click="$router.push('/bazi')">
                添加新八字
              </el-button>
            </div>
          </template>
          
          <el-table 
            :data="userStore.baziRecords" 
            style="width: 100%"
            v-loading="loadingBazi"
          >
            <el-table-column prop="year" label="年柱" />
            <el-table-column prop="month" label="月柱" />
            <el-table-column prop="day" label="日柱" />
            <el-table-column prop="hour" label="时柱" />
            <el-table-column prop="gender" label="性别" />
            <el-table-column prop="created_at" label="创建时间" />
            <el-table-column label="操作" width="180">
              <template #default="scope">
                <el-button
                  size="small"
                  @click="handleViewBaziFortune(scope.row)"
                  type="primary"
                >
                  查看运势
                </el-button>
                <el-button
                  size="small"
                  type="danger"
                  @click="handleDeleteBazi(scope.row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <!-- 算命记录 -->
        <el-card class="fortune-records-card" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span>算命记录</span>
              <div>
                <el-select v-model="filterType" placeholder="筛选类型" style="width: 120px; margin-right: 10px;">
                  <el-option label="全部" value="" />
                  <el-option label="今日运势" value="daily" />
                  <el-option label="姻缘运势" value="love" />
                  <el-option label="事业运势" value="career" />
                  <el-option label="财运运势" value="wealth" />
                  <el-option label="健康运势" value="health" />
                </el-select>
                <el-button @click="handleRefresh">刷新</el-button>
              </div>
            </div>
          </template>
          
          <el-table 
            :data="filteredFortuneRecords" 
            style="width: 100%"
            v-loading="loadingFortune"
          >
            <el-table-column prop="fortune_type" label="算命类型">
              <template #default="scope">
                <el-tag :type="getFortuneTypeTag(scope.row.fortune_type)">
                  {{ getFortuneTypeName(scope.row.fortune_type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="结果等级">
              <template #default="scope">
                <span :class="getResultLevelClass(scope.row.result.level)">
                  {{ scope.row.result.level }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="result.description" label="结果描述" show-overflow-tooltip />
            <el-table-column prop="created_at" label="算命时间" width="180" />
            <el-table-column label="操作" width="180">
              <template #default="scope">
                <el-button
                  size="small"
                  @click="handleViewDetail(scope.row)"
                  type="primary"
                >
                  查看详情
                </el-button>
                <el-button
                  size="small"
                  type="danger"
                  @click="handleDeleteFortune(scope.row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <!-- 爱情运势记录 -->
        <el-card class="love-records-card" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span>爱情运势记录</span>
              <el-button @click="handleRefreshLove">刷新</el-button>
            </div>
          </template>
          
          <el-table 
            :data="loveFortunes" 
            style="width: 100%"
            v-loading="loadingLove"
          >
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="user_id" label="用户ID" width="100" />
            <el-table-column prop="bazi_id" label="八字ID" width="100" />
            <el-table-column prop="love_level" label="爱情等级" />
            <el-table-column prop="romantic_opportunity" label="浪漫机会" show-overflow-tooltip />
            <el-table-column prop="compatibility_partner" label="最佳配对" />
            <el-table-column prop="created_at" label="创建时间" width="180" />
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button size="small" type="danger" @click="handleDeleteLove(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <!-- 运势分类管理 -->
        <el-card class="categories-card" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span>运势分类管理</span>
              <div>
                <el-button type="primary" @click="handleAddCategory">添加分类</el-button>
                <el-button @click="handleRefreshCategories">刷新</el-button>
              </div>
            </div>
          </template>
          
          <el-table 
            :data="categories" 
            style="width: 100%"
            v-loading="loadingCategories"
          >
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="分类名称" />
            <el-table-column prop="description" label="描述" show-overflow-tooltip />
            <el-table-column prop="icon" label="图标" />
            <el-table-column prop="color" label="颜色" />
            <el-table-column prop="is_active" label="是否启用">
              <template #default="scope">
                <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
                  {{ scope.row.is_active ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180" />
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button size="small" type="danger" @click="handleDeleteCategory(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <!-- 算命结果详情对话框 -->
        <el-dialog
          v-model="showDetail"
          title="算命结果详情"
          width="500px"
        >
          <div v-if="currentDetail" class="fortune-detail">
            <div class="detail-header">
              <h3 :class="getResultLevelClass(currentDetail.result.level)">
                {{ currentDetail.result.level }} - {{ getFortuneTypeName(currentDetail.fortune_type) }}
              </h3>
              <p class="detail-time">{{ formatTime(currentDetail.created_at) }}</p>
            </div>
            
            <div class="detail-content">
              <p class="description">{{ currentDetail.result.description }}</p>
              
              <div v-if="currentDetail.result.lucky_color" class="detail-items">
                <el-row :gutter="20">
                  <el-col :span="12" v-if="currentDetail.result.lucky_color">
                    <div class="detail-item">
                      <span class="label">幸运颜色：</span>
                      <span class="value">{{ currentDetail.result.lucky_color }}</span>
                    </div>
                  </el-col>
                  <el-col :span="12" v-if="currentDetail.result.lucky_number">
                    <div class="detail-item">
                      <span class="label">幸运数字：</span>
                      <span class="value">{{ currentDetail.result.lucky_number }}</span>
                    </div>
                  </el-col>
                </el-row>
                
                <div v-if="currentDetail.result.advice" class="advice">
                  <h4>建议：</h4>
                  <p>{{ currentDetail.result.advice }}</p>
                </div>
                
                <div v-if="currentDetail.result.meeting_chance" class="meeting-chance">
                  <h4>相遇机会：</h4>
                  <p>{{ currentDetail.result.meeting_chance }}</p>
                </div>
                
                <div v-if="currentDetail.result.compatibility" class="compatibility">
                  <h4>最佳配对：</h4>
                  <p>{{ currentDetail.result.compatibility }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <template #footer>
            <el-button @click="showDetail = false">关闭</el-button>
          </template>
        </el-dialog>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

const router = useRouter()
const userStore = useUserStore()

const loadingBazi = ref(false)
const loadingFortune = ref(false)
const loadingLove = ref(false)
const loadingCategories = ref(false)
const filterType = ref('')
const showDetail = ref(false)
const currentDetail = ref(null)

// 新增数据
const loveFortunes = ref([])
const categories = ref([])

// API基础URL
const API_BASE = 'http://localhost:8000'

const filteredFortuneRecords = computed(() => {
  if (!filterType.value) {
    return userStore.fortuneRecords
  }
  return userStore.fortuneRecords.filter(record => record.fortune_type === filterType.value)
})

onMounted(async () => {
  await loadRecords()
})

const loadRecords = async () => {
  loadingBazi.value = true
  loadingFortune.value = true
  loadingLove.value = true
  loadingCategories.value = true
  
  try {
    await Promise.all([
      userStore.getBaziRecords(),
      userStore.getFortuneRecords(),
      loadLoveFortunes(),
      loadCategories()
    ])
  } catch (error) {
    ElMessage.error('加载数据失败：' + error.message)
  }
  
  loadingBazi.value = false
  loadingFortune.value = false
  loadingLove.value = false
  loadingCategories.value = false
}

// 加载爱情运势
const loadLoveFortunes = async () => {
  try {
    const response = await axios.get(`${API_BASE}/api/admin/love-fortunes`)
    loveFortunes.value = response.data
  } catch (error) {
    ElMessage.error('加载爱情运势失败：' + error.message)
  }
}

// 加载运势分类
const loadCategories = async () => {
  try {
    const response = await axios.get(`${API_BASE}/api/admin/fortune-categories`)
    categories.value = response.data
  } catch (error) {
    ElMessage.error('加载运势分类失败：' + error.message)
  }
}

const handleRefresh = () => {
  loadRecords()
}

const handleRefreshLove = () => {
  loadLoveFortunes()
}

const handleRefreshCategories = () => {
  loadCategories()
}

const handleViewBaziFortune = (baziRecord) => {
  userStore.currentBazi = baziRecord
  router.push('/fortune')
}

const handleViewDetail = (record) => {
  currentDetail.value = record
  showDetail.value = true
}

// 八字记录删除方法
const handleDeleteBazi = async (bazi) => {
  try {
    await ElMessageBox.confirm('确定要删除这条八字记录吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`${API_BASE}/api/admin/bazi-records/${bazi.id}`)
    ElMessage.success('八字记录删除成功')
    await userStore.getBaziRecords() // 重新加载八字记录
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败：' + error.message)
    }
  }
}

// 算命记录删除方法
const handleDeleteFortune = async (fortune) => {
  try {
    await ElMessageBox.confirm('确定要删除这条算命记录吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`${API_BASE}/api/admin/fortune-records/${fortune.id}`)
    ElMessage.success('算命记录删除成功')
    await userStore.getFortuneRecords() // 重新加载算命记录
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败：' + error.message)
    }
  }
}

// 爱情运势删除方法
const handleDeleteLove = async (love) => {
  try {
    await ElMessageBox.confirm('确定要删除这条爱情运势记录吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`${API_BASE}/api/admin/love-fortunes/${love.id}`)
    ElMessage.success('爱情运势删除成功')
    loadLoveFortunes()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败：' + error.message)
    }
  }
}

// 运势分类操作方法
const handleAddCategory = async () => {
  try {
    const result = await ElMessageBox.prompt('请输入分类名称', '添加运势分类', {
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    
    await axios.post(`${API_BASE}/api/admin/fortune-categories`, {
      name: result.value,
      description: '新的运势分类',
      is_active: true
    })
    
    ElMessage.success('分类添加成功')
    loadCategories()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('添加失败：' + error.message)
    }
  }
}

const handleDeleteCategory = async (category) => {
  try {
    await ElMessageBox.confirm('确定要删除这个运势分类吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`${API_BASE}/api/admin/fortune-categories/${category.id}`)
    ElMessage.success('分类删除成功')
    loadCategories()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败：' + error.message)
    }
  }
}

const getFortuneTypeName = (type) => {
  const typeMap = {
    daily: '今日运势',
    love: '姻缘运势',
    career: '事业运势',
    wealth: '财运运势',
    health: '健康运势'
  }
  return typeMap[type] || type
}

const getFortuneTypeTag = (type) => {
  const tagMap = {
    daily: 'primary',
    love: 'danger',
    career: 'success',
    wealth: 'warning',
    health: 'info'
  }
  return tagMap[type] || 'info'
}

const getResultLevelClass = (level) => {
  const classMap = {
    '大吉': 'great-luck',
    '吉': 'good-luck',
    '中吉': 'medium-luck',
    '小吉': 'small-luck',
    '平': 'normal-luck',
    '凶': 'bad-luck',
    '大凶': 'very-bad-luck'
  }
  return classMap[level] || 'normal-luck'
}

const formatTime = (timeString) => {
  return new Date(timeString).toLocaleString('zh-CN')
}
</script>

<style scoped>
.records-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.fortune-detail .detail-header {
  text-align: center;
  margin-bottom: 20px;
}

.detail-header h3 {
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
}

.detail-time {
  color: #666;
  font-size: 14px;
}

.description {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.detail-items {
  margin-top: 20px;
}

.detail-item {
  margin-bottom: 10px;
}

.detail-item .label {
  font-weight: bold;
  color: #666;
}

.detail-item .value {
  color: #333;
}

.advice,
.meeting-chance,
.compatibility {
  margin-top: 15px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 5px;
}

.advice h4,
.meeting-chance h4,
.compatibility h4 {
  margin-bottom: 5px;
  color: #333;
}

/* 结果等级样式 */
.great-luck { color: #409eff; background-color: #f0f9ff; }
.good-luck { color: #67c23a; background-color: #f0f9e6; }
.medium-luck { color: #e6a23c; background-color: #fdf6ec; }
.small-luck { color: #f56c6c; background-color: #fef0f0; }
.normal-luck { color: #909399; background-color: #f4f4f5; }
.bad-luck { color: #f56c6c; background-color: #fef0f0; }
.very-bad-luck { color: #f56c6c; background-color: #fef0f0; }
</style>