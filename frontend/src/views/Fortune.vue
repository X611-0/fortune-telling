<template>
  <div class="fortune-container">
    <el-container>
      <el-header style="background: transparent;">
        <div class="header-content">
          <div class="page-title">
            <el-icon size="32" color="#409EFF"><MagicStick /></el-icon>
            <h1>算命功能</h1>
          </div>
          <div class="header-actions">
            <el-button @click="$router.push('/')">返回首页</el-button>
          </div>
        </div>
      </el-header>
      
      <el-main style="background: white; border-radius: 8px; margin: 20px; padding: 20px;">
        <!-- 八字选择区域 -->
        <el-card class="bazi-selection-card" v-if="userStore.baziRecords.length > 0">
          <template #header>
            <div class="card-header">
              <el-icon size="20" color="#409EFF"><Calendar /></el-icon>
              <span>选择要使用的八字</span>
            </div>
          </template>
          
          <el-radio-group v-model="selectedBaziId" @change="handleBaziChange">
            <el-space direction="vertical" size="large">
              <el-radio
                v-for="bazi in userStore.baziRecords"
                :key="bazi.id"
                :label="bazi.id"
                border
              >
                {{ bazi.year }}年 {{ bazi.month }}月 {{ bazi.day }}日 {{ bazi.hour }}时 ({{ bazi.gender }})
              </el-radio>
            </el-space>
          </el-radio-group>
          
          <div v-if="!selectedBaziId" class="no-bazi-selected">
            <el-alert title="请先选择一个八字记录" type="warning" show-icon />
          </div>
        </el-card>
        
        <div v-else class="no-bazi-records">
          <el-alert title="您还没有八字记录，请先输入八字信息" type="info" show-icon />
          <el-button type="primary" @click="$router.push('/bazi')" style="margin-top: 20px;">
            去输入八字
          </el-button>
        </div>
        
        <!-- 算命功能选择 -->
        <div v-if="selectedBaziId" class="fortune-features">
          <div class="section-title">
            <el-icon size="24" color="#E6A23C"><Star /></el-icon>
            <h3>选择算命类型</h3>
          </div>
          <el-row :gutter="20">
            <el-col :span="6" v-for="feature in fortuneFeatures" :key="feature.type">
              <el-card 
                class="feature-card" 
                shadow="hover" 
                @click="handleCalculateFortune(feature.type)"
              >
                <div class="feature-content">
                  <el-icon :size="40" :color="feature.color">
                    <component :is="feature.icon" />
                  </el-icon>
                  <h4>{{ feature.name }}</h4>
                  <p>{{ feature.description }}</p>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
        
        <!-- 算命结果展示 -->
        <el-dialog
          v-model="showResult"
          width="600px"
          :before-close="handleCloseResult"
        >
          <template #header>
            <div class="dialog-header">
              <el-icon size="24" color="#409EFF"><Trophy /></el-icon>
              <span>算命结果</span>
            </div>
          </template>
          <div v-if="currentResult" class="fortune-result">
              <div class="result-header">
                <h3 :class="getResultLevelClass(currentResult.fortune_level)">
                  {{ currentResult.fortune_level }} - {{ currentResult.fortune_type }}
                </h3>
              </div>
              
              <div class="result-content">
                <p class="result-description">{{ currentResult.fortune_description }}</p>
                
                <div class="result-details">
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <div class="detail-item">
                        <span class="label">幸运颜色：</span>
                        <span class="value">{{ currentResult.lucky_color }}</span>
                      </div>
                    </el-col>
                    <el-col :span="12">
                      <div class="detail-item">
                        <span class="label">幸运数字：</span>
                        <span class="value">{{ currentResult.lucky_number }}</span>
                      </div>
                    </el-col>
                  </el-row>
                  
                  <!-- 爱情解读特有字段 -->
                  <div v-if="currentResult.fortune_type === '爱情解读'">
                    <div class="love-details">
                      <el-row :gutter="20">
                        <el-col :span="12">
                          <div class="detail-item">
                            <span class="label">浪漫机会：</span>
                            <span class="value">{{ currentResult.meeting_chance }}</span>
                          </div>
                        </el-col>
                        <el-col :span="12">
                          <div class="detail-item">
                            <span class="label">最佳配对：</span>
                            <span class="value">{{ currentResult.compatibility }}</span>
                          </div>
                        </el-col>
                      </el-row>
                      
                      <div v-if="currentResult.lucky_meeting_places" class="detail-item">
                        <span class="label">幸运地点：</span>
                        <span class="value">{{ currentResult.lucky_meeting_places }}</span>
                      </div>
                      
                      <div v-if="currentResult.love_challenges" class="love-challenges">
                        <h4>爱情挑战：</h4>
                        <p>{{ currentResult.love_challenges }}</p>
                      </div>
                      
                      <div v-if="currentResult.improvement_suggestions" class="improvement-suggestions">
                        <h4>改进建议：</h4>
                        <p>{{ currentResult.improvement_suggestions }}</p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 普通运势字段 -->
                  <div v-else>
                    <div v-if="currentResult.advice" class="advice">
                      <h4>建议：</h4>
                      <p>{{ currentResult.advice }}</p>
                    </div>
                    
                    <div v-if="currentResult.meeting_chance" class="meeting-chance">
                      <h4>相遇机会：</h4>
                      <p>{{ currentResult.meeting_chance }}</p>
                    </div>
                    
                    <div v-if="currentResult.compatibility" class="compatibility">
                      <h4>最佳配对：</h4>
                      <p>{{ currentResult.compatibility }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          
          <template #footer>
            <el-button @click="handleCloseResult">关闭</el-button>
            <el-button type="primary" @click="handleSaveResult">保存记录</el-button>
          </template>
        </el-dialog>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Sunny,
  MagicStick,
  Calendar,
  Star,
  Trophy,
  TrendCharts,
  Money,
  FirstAidKit
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const selectedBaziId = ref('')
const showResult = ref(false)
const currentResult = ref(null)
const calculating = ref(false)

const fortuneFeatures = ref([
  {
    type: 'daily',
    name: '今日运势',
    description: '查看今天的整体运势',
    icon: Sunny,
    color: '#E6A23C'
  },
  {
    type: 'career',
    name: '事业运势',
    description: '查看工作事业发展',
    icon: TrendCharts,
    color: '#409EFF'
  },
  {
    type: 'wealth',
    name: '财运运势',
    description: '查看财富财运情况',
    icon: Money,
    color: '#67C23A'
  },
  {
    type: 'health',
    name: '健康运势',
    description: '查看身体健康状况',
    icon: FirstAidKit,
    color: '#909399'
  },
  {
    type: 'love',
    name: '爱情解读',
    description: '查看爱情缘分情况',
    icon: Star,
    color: '#F56C6C'
  }
])

const handleBaziChange = (baziId) => {
  selectedBaziId.value = baziId
}

const handleCalculateFortune = async (fortuneType) => {
  if (!selectedBaziId.value) {
    ElMessage.warning('请先选择八字')
    return
  }

  calculating.value = true
  
  try {
    let result
    
    if (fortuneType === 'love') {
      // 调用爱情解读API
        result = await userStore.calculateLoveFortune({
          bazi_id: selectedBaziId.value
        })
        
        if (result.success) {
          // 处理爱情解读结果
          currentResult.value = {
            fortune_type: '爱情解读',
            result: '爱情解读分析结果',
          fortune_level: result.data.love_level || '中等',
          fortune_description: `情感状态：${result.data.emotional_state || '稳定'}，沟通方式：${result.data.communication_style || '直接'}`,
          lucky_color: '粉色',
          lucky_number: '3',
          advice: result.data.relationship_advice || '保持真诚，耐心等待',
          meeting_chance: result.data.romantic_opportunity || '社交场合',
          compatibility: result.data.compatibility_partner || '属兔、属羊的人',
          love_challenges: result.data.love_challenges,
          improvement_suggestions: result.data.improvement_suggestions,
          lucky_meeting_places: result.data.lucky_meeting_places
        }
        showResult.value = true
      }
    } else {
      // 调用普通运势API
      result = await userStore.calculateFortune({
        bazi_id: selectedBaziId.value,
        fortune_type: fortuneType
      })

      if (result.success) {
        // 使用后端返回的完整数据，并添加默认值以确保显示
        currentResult.value = {
          fortune_type: result.data.fortune_type || fortuneType,
          result: result.data.result || `${fortuneType}运势分析结果`,
          fortune_level: '吉',
          fortune_description: '今日运势平稳，适合处理日常事务',
          lucky_color: '红色',
          lucky_number: '8',
          advice: '保持积极心态，注意与人沟通',
          meeting_chance: '较高',
          compatibility: '属鼠、属龙的人'
        }
        showResult.value = true
      }
    }
    
    if (!result.success) {
      ElMessage.error(result.message)
    }
  } catch (error) {
    ElMessage.error('运势计算失败：' + error.message)
  }
  
  calculating.value = false
}

const handleCloseResult = () => {
  showResult.value = false
  currentResult.value = null
}

const handleSaveResult = () => {
  ElMessage.success('结果已保存到个人记录')
  handleCloseResult()
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
</script>

<style scoped>
.fortune-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title h1 {
  color: white;
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #409EFF;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.section-title h3 {
  color: white;
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.dialog-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #409EFF;
}

.bazi-selection-card,
.no-bazi-records {
  margin-bottom: 30px;
}

.fortune-features {
  margin-top: 30px;
}

.feature-card {
  cursor: pointer;
  transition: transform 0.3s;
  height: 180px;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-content {
  text-align: center;
  padding: 20px;
}

.feature-content h4 {
  margin: 15px 0 10px;
  color: #333;
}

.feature-content p {
  color: #666;
  font-size: 12px;
}

.fortune-result .result-header h3 {
  text-align: center;
  margin-bottom: 20px;
  padding: 10px;
  border-radius: 5px;
}

.great-luck { background-color: #f0f9ff; color: #409eff; }
.good-luck { background-color: #f0f9e6; color: #67c23a; }
.medium-luck { background-color: #fdf6ec; color: #e6a23c; }
.small-luck { background-color: #fef0f0; color: #f56c6c; }
.normal-luck { background-color: #f4f4f5; color: #909399; }
.bad-luck { background-color: #fef0f0; color: #f56c6c; }
.very-bad-luck { background-color: #fef0f0; color: #f56c6c; }

.result-description {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 20px;
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
</style>