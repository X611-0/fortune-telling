<template>
  <div class="bazi-container">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>八字输入</h1>
          <div class="header-actions">
            <el-button @click="$router.push('/')">返回首页</el-button>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <el-card class="bazi-form-card">
          <template #header>
            <div class="card-header">
              <span>请输入您的生辰八字信息</span>
            </div>
          </template>
          
          <el-form :model="form" :rules="rules" ref="baziForm" label-width="100px">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="年柱" prop="year">
                  <el-select v-model="form.year" placeholder="请选择年份" style="width: 100%">
                    <el-option
                      v-for="year in years"
                      :key="`year-${year}`"
                      :label="year"
                      :value="year"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="月柱" prop="month">
                  <el-select v-model="form.month" placeholder="请选择月份" style="width: 100%">
                    <el-option
                      v-for="month in months"
                      :key="`month-${month}`"
                      :label="month"
                      :value="month"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="日柱" prop="day">
                  <el-select v-model="form.day" placeholder="请选择日期" style="width: 100%">
                    <el-option
                      v-for="day in days"
                      :key="`day-${day}`"
                      :label="day"
                      :value="day"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="时柱" prop="hour">
                  <el-select v-model="form.hour" placeholder="请选择时辰" style="width: 100%">
                    <el-option
                      v-for="hour in hours"
                      :key="`hour-${hour}`"
                      :label="hour"
                      :value="hour"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="form.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="handleSubmit" :loading="loading">
                保存八字信息
              </el-button>
              <el-button @click="handleReset">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
        
        <!-- 八字记录列表 -->
        <el-card class="records-card" v-if="userStore.baziRecords.length > 0">
          <template #header>
            <div class="card-header">
              <span>您的八字记录</span>
            </div>
          </template>
          
          <el-table :data="userStore.baziRecords" style="width: 100%">
            <el-table-column prop="year" label="年柱" />
            <el-table-column prop="month" label="月柱" />
            <el-table-column prop="day" label="日柱" />
            <el-table-column prop="hour" label="时柱" />
            <el-table-column prop="gender" label="性别" />
            <el-table-column prop="created_at" label="创建时间" />
            <el-table-column label="操作">
              <template #default="scope">
                <el-button
                  size="small"
                  @click="handleUseBazi(scope.row)"
                  type="primary"
                >
                  使用此八字
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const baziForm = ref()
const loading = ref(false)

// 生成八字选项数据
const years = ref(Array.from({length: 60}, (_, i) => `甲子${i+1}`))
const months = ref(['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月'])
const days = ref(Array.from({length: 30}, (_, i) => `初${i+1}`))
const hours = ref(['子时', '丑时', '寅时', '卯时', '辰时', '巳时', '午时', '未时', '申时', '酉时', '戌时', '亥时'])

const form = ref({
  year: '',
  month: '',
  day: '',
  hour: '',
  gender: ''
})

const rules = {
  year: [{ required: true, message: '请选择年柱', trigger: 'change' }],
  month: [{ required: true, message: '请选择月柱', trigger: 'change' }],
  day: [{ required: true, message: '请选择日柱', trigger: 'change' }],
  hour: [{ required: true, message: '请选择时柱', trigger: 'change' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }]
}

onMounted(async () => {
  await userStore.getBaziRecords()
})

const handleSubmit = async () => {
  if (!baziForm.value) return
  
  await baziForm.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      const result = await userStore.createBaziRecord(form.value)
      
      if (result.success) {
        ElMessage.success('八字信息保存成功')
        handleReset()
      } else {
        ElMessage.error(result.message)
      }
      loading.value = false
    }
  })
}

const handleReset = () => {
  if (baziForm.value) {
    baziForm.value.resetFields()
  }
}

const handleUseBazi = (baziRecord) => {
  // 保存当前选择的八字到状态管理，然后跳转到算命页面
  userStore.currentBazi = baziRecord
  router.push('/fortune')
}
</script>

<style scoped>
.bazi-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.bazi-form-card {
  margin-bottom: 20px;
}

.records-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>