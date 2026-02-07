<template>
  <div class="admin-container">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>数据库管理</h1>
          <div class="header-actions">
            <el-button @click="$router.push('/')">返回首页</el-button>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <el-tabs v-model="activeTab" type="card">
          <!-- 用户管理 -->
          <el-tab-pane label="用户管理" name="users">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>用户列表</span>
                  <el-button type="primary" @click="handleAddUser">添加用户</el-button>
                </div>
              </template>
              
              <el-table :data="users" v-loading="loading.users">
                <el-table-column prop="id" label="ID" width="80" />
                <el-table-column prop="username" label="用户名" />
                <el-table-column prop="email" label="邮箱" />
                <el-table-column prop="created_at" label="创建时间" width="180" />
                <el-table-column label="操作" width="200">
                  <template #default="scope">
                    <el-button size="small" @click="handleEditUser(scope.row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDeleteUser(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>
          
          <!-- 八字记录管理 -->
          <el-tab-pane label="八字记录" name="bazi">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>八字记录列表</span>
                  <el-button type="primary" @click="handleAddBazi">添加八字记录</el-button>
                </div>
              </template>
              
              <el-table :data="baziRecords" v-loading="loading.bazi">
                <el-table-column prop="id" label="ID" width="80" />
                <el-table-column prop="user_id" label="用户ID" width="100" />
                <el-table-column prop="year" label="年柱" />
                <el-table-column prop="month" label="月柱" />
                <el-table-column prop="day" label="日柱" />
                <el-table-column prop="hour" label="时柱" />
                <el-table-column prop="gender" label="性别" />
                <el-table-column prop="created_at" label="创建时间" width="180" />
                <el-table-column label="操作" width="200">
                  <template #default="scope">
                    <el-button size="small" @click="handleEditBazi(scope.row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDeleteBazi(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>
          
          <!-- 算命记录管理 -->
          <el-tab-pane label="算命记录" name="fortune">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>算命记录列表</span>
                  <el-button type="primary" @click="handleAddFortune">添加算命记录</el-button>
                </div>
              </template>
              
              <el-table :data="fortuneRecords" v-loading="loading.fortune">
                <el-table-column prop="id" label="ID" width="80" />
                <el-table-column prop="user_id" label="用户ID" width="100" />
                <el-table-column prop="bazi_id" label="八字ID" width="100" />
                <el-table-column prop="category_id" label="分类ID" width="100" />
                <el-table-column prop="result" label="结果" show-overflow-tooltip />
                <el-table-column prop="created_at" label="创建时间" width="180" />
                <el-table-column label="操作" width="200">
                  <template #default="scope">
                    <el-button size="small" @click="handleEditFortune(scope.row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDeleteFortune(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>
          
          <!-- 爱情运势管理 -->
          <el-tab-pane label="爱情运势" name="love">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>爱情运势列表</span>
                  <el-button type="primary" @click="handleAddLove">添加爱情运势</el-button>
                </div>
              </template>
              
              <el-table :data="loveFortunes" v-loading="loading.love">
                <el-table-column prop="id" label="ID" width="80" />
                <el-table-column prop="user_id" label="用户ID" width="100" />
                <el-table-column prop="bazi_id" label="八字ID" width="100" />
                <el-table-column prop="love_level" label="爱情等级" />
                <el-table-column prop="romantic_opportunity" label="浪漫机会" show-overflow-tooltip />
                <el-table-column prop="compatibility_partner" label="最佳配对" />
                <el-table-column prop="created_at" label="创建时间" width="180" />
                <el-table-column label="操作" width="200">
                  <template #default="scope">
                    <el-button size="small" @click="handleEditLove(scope.row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDeleteLove(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>
          
          <!-- 运势分类管理 -->
          <el-tab-pane label="运势分类" name="categories">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>运势分类列表</span>
                  <el-button type="primary" @click="handleAddCategory">添加分类</el-button>
                </div>
              </template>
              
              <el-table :data="categories" v-loading="loading.categories">
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
                <el-table-column label="操作" width="200">
                  <template #default="scope">
                    <el-button size="small" @click="handleEditCategory(scope.row)">编辑</el-button>
                    <el-button size="small" type="danger" @click="handleDeleteCategory(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const activeTab = ref('users')
const loading = ref({
  users: false,
  bazi: false,
  fortune: false,
  love: false,
  categories: false
})

// 数据
const users = ref([])
const baziRecords = ref([])
const fortuneRecords = ref([])
const loveFortunes = ref([])
const categories = ref([])

// API基础URL
const API_BASE = 'http://localhost:8000'

onMounted(async () => {
  await loadAllData()
})

const loadAllData = async () => {
  try {
    loading.value = {
      users: true,
      bazi: true,
      fortune: true,
      love: true,
      categories: true
    }
    
    // 调用真实的后端API获取数据
    const [usersRes, baziRes, fortuneRes, loveRes, categoriesRes] = await Promise.all([
      axios.get(`${API_BASE}/admin/users`),
      axios.get(`${API_BASE}/admin/bazi-records`),
      axios.get(`${API_BASE}/admin/fortune-records`),
      axios.get(`${API_BASE}/admin/love-fortunes`),
      axios.get(`${API_BASE}/admin/fortune-categories`)
    ])
    
    users.value = usersRes.data
    baziRecords.value = baziRes.data
    fortuneRecords.value = fortuneRes.data
    loveFortunes.value = loveRes.data
    categories.value = categoriesRes.data
    
  } catch (error) {
    ElMessage.error('加载数据失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = {
      users: false,
      bazi: false,
      fortune: false,
      love: false,
      categories: false
    }
  }
}

// 添加操作
const handleAddUser = async () => {
  try {
    const { value: formData } = await ElMessageBox.prompt('请输入用户名、邮箱和密码（格式：用户名,邮箱,密码）', '添加用户', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputPattern: /^[^,]+,[^,]+,[^,]+$/,
      inputErrorMessage: '格式错误，请使用：用户名,邮箱,密码'
    })
    
    const [username, email, password] = formData.split(',')
    
    await axios.post(`${API_BASE}/admin/users`, {
      username: username.trim(),
      email: email.trim(),
      password: password.trim()
    })
    
    ElMessage.success('用户添加成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('添加用户失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const handleAddBazi = async () => {
  try {
    const { value: formData } = await ElMessageBox.prompt('请输入用户ID、年柱、月柱、日柱、时柱、性别（格式：用户ID,年柱,月柱,日柱,时柱,性别）', '添加八字记录', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputPattern: /^\d+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+$/,
      inputErrorMessage: '格式错误，请使用：用户ID,年柱,月柱,日柱,时柱,性别'
    })
    
    const [user_id, year, month, day, hour, gender] = formData.split(',')
    
    await axios.post(`${API_BASE}/admin/bazi-records`, {
      user_id: parseInt(user_id),
      year: year.trim(),
      month: month.trim(),
      day: day.trim(),
      hour: hour.trim(),
      gender: gender.trim()
    })
    
    ElMessage.success('八字记录添加成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('添加八字记录失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const handleAddFortune = async () => {
  try {
    const { value: formData } = await ElMessageBox.prompt('请输入用户ID、八字ID、分类ID、结果（格式：用户ID,八字ID,分类ID,结果）', '添加算命记录', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputPattern: /^\d+,\d+,\d+,[^,]+$/,
      inputErrorMessage: '格式错误，请使用：用户ID,八字ID,分类ID,结果'
    })
    
    const [user_id, bazi_id, category_id, result] = formData.split(',')
    
    await axios.post(`${API_BASE}/admin/fortune-records`, {
      user_id: parseInt(user_id),
      bazi_id: parseInt(bazi_id),
      category_id: parseInt(category_id),
      result: result.trim()
    })
    
    ElMessage.success('算命记录添加成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('添加算命记录失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const handleAddLove = async () => {
  try {
    const { value: formData } = await ElMessageBox.prompt('请输入用户ID、八字ID、爱情等级、浪漫机会、最佳配对（格式：用户ID,八字ID,爱情等级,浪漫机会,最佳配对）', '添加爱情运势', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputPattern: /^\d+,\d+,[^,]+,[^,]+,[^,]+$/,
      inputErrorMessage: '格式错误，请使用：用户ID,八字ID,爱情等级,浪漫机会,最佳配对'
    })
    
    const [user_id, bazi_id, love_level, romantic_opportunity, compatibility_partner] = formData.split(',')
    
    await axios.post(`${API_BASE}/admin/love-fortunes`, {
      user_id: parseInt(user_id),
      bazi_id: parseInt(bazi_id),
      love_level: love_level.trim(),
      romantic_opportunity: romantic_opportunity.trim(),
      compatibility_partner: compatibility_partner.trim()
    })
    
    ElMessage.success('爱情运势添加成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('添加爱情运势失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const handleAddCategory = async () => {
  try {
    const { value: formData } = await ElMessageBox.prompt('请输入分类名称、描述、图标、颜色、是否启用（格式：名称,描述,图标,颜色,是否启用）', '添加分类', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputPattern: /^[^,]+,[^,]+,[^,]+,[^,]+,(true|false)$/,
      inputErrorMessage: '格式错误，请使用：名称,描述,图标,颜色,是否启用(true/false)'
    })
    
    const [name, description, icon, color, is_active] = formData.split(',')
    
    await axios.post(`${API_BASE}/admin/fortune-categories`, {
      name: name.trim(),
      description: description.trim(),
      icon: icon.trim(),
      color: color.trim(),
      is_active: is_active.trim().toLowerCase() === 'true'
    })
    
    ElMessage.success('分类添加成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('添加分类失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

// 编辑操作
const handleEditUser = async (user) => {
  try {
    const { value: newData } = await ElMessageBox.prompt(`编辑用户 ${user.username}（格式：新用户名,新邮箱）`, '编辑用户', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputValue: `${user.username},${user.email}`,
      inputPattern: /^[^,]+,[^,]+$/,
      inputErrorMessage: '格式错误，请使用：用户名,邮箱'
    })
    
    const [username, email] = newData.split(',')
    
    await axios.put(`${API_BASE}/admin/users/${user.id}`, {
      username: username.trim(),
      email: email.trim()
    })
    
    ElMessage.success('用户更新成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('更新用户失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const handleEditBazi = async (bazi) => {
  try {
    const { value: newData } = await ElMessageBox.prompt(`编辑八字记录 ${bazi.id}（格式：年柱,月柱,日柱,时柱,性别）`, '编辑八字记录', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputValue: `${bazi.year},${bazi.month},${bazi.day},${bazi.hour},${bazi.gender}`,
      inputPattern: /^[^,]+,[^,]+,[^,]+,[^,]+,[^,]+$/,
      inputErrorMessage: '格式错误，请使用：年柱,月柱,日柱,时柱,性别'
    })
    
    const [year, month, day, hour, gender] = newData.split(',')
    
    await axios.put(`${API_BASE}/admin/bazi-records/${bazi.id}`, {
      year: year.trim(),
      month: month.trim(),
      day: day.trim(),
      hour: hour.trim(),
      gender: gender.trim()
    })
    
    ElMessage.success('八字记录更新成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('更新八字记录失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const handleEditFortune = async (fortune) => {
  try {
    const { value: newData } = await ElMessageBox.prompt(`编辑算命记录 ${fortune.id}（格式：分类ID,结果）`, '编辑算命记录', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputValue: `${fortune.category_id},${fortune.result}`,
      inputPattern: /^\d+,[^,]+$/,
      inputErrorMessage: '格式错误，请使用：分类ID,结果'
    })
    
    const [category_id, result] = newData.split(',')
    
    await axios.put(`${API_BASE}/admin/fortune-records/${fortune.id}`, {
      category_id: parseInt(category_id),
      result: result.trim()
    })
    
    ElMessage.success('算命记录更新成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('更新算命记录失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const handleEditLove = async (love) => {
  try {
    const { value: newData } = await ElMessageBox.prompt(`编辑爱情运势 ${love.id}（格式：爱情等级,浪漫机会,最佳配对）`, '编辑爱情运势', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputValue: `${love.love_level},${love.romantic_opportunity},${love.compatibility_partner}`,
      inputPattern: /^[^,]+,[^,]+,[^,]+$/,
      inputErrorMessage: '格式错误，请使用：爱情等级,浪漫机会,最佳配对'
    })
    
    const [love_level, romantic_opportunity, compatibility_partner] = newData.split(',')
    
    await axios.put(`${API_BASE}/admin/love-fortunes/${love.id}`, {
      love_level: love_level.trim(),
      romantic_opportunity: romantic_opportunity.trim(),
      compatibility_partner: compatibility_partner.trim()
    })
    
    ElMessage.success('爱情运势更新成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('更新爱情运势失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const handleEditCategory = async (category) => {
  try {
    const { value: newData } = await ElMessageBox.prompt(`编辑分类 ${category.name}（格式：名称,描述,图标,颜色,是否启用）`, '编辑分类', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputValue: `${category.name},${category.description},${category.icon},${category.color},${category.is_active}`,
      inputPattern: /^[^,]+,[^,]+,[^,]+,[^,]+,(true|false)$/,
      inputErrorMessage: '格式错误，请使用：名称,描述,图标,颜色,是否启用(true/false)'
    })
    
    const [name, description, icon, color, is_active] = newData.split(',')
    
    await axios.put(`${API_BASE}/admin/fortune-categories/${category.id}`, {
      name: name.trim(),
      description: description.trim(),
      icon: icon.trim(),
      color: color.trim(),
      is_active: is_active.trim().toLowerCase() === 'true'
    })
    
    ElMessage.success('分类更新成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('更新分类失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

// 删除操作
const handleDeleteUser = async (user) => {
  try {
    await ElMessageBox.confirm(`确定删除用户 "${user.username}" 吗？`, '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`${API_BASE}/admin/users/${user.id}`)
    ElMessage.success('删除用户成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除用户失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const handleDeleteBazi = async (bazi) => {
  try {
    await ElMessageBox.confirm('确定删除这条八字记录吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`${API_BASE}/admin/bazi-records/${bazi.id}`)
    ElMessage.success('删除八字记录成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除八字记录失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const handleDeleteFortune = async (fortune) => {
  try {
    await ElMessageBox.confirm('确定删除这条算命记录吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`${API_BASE}/admin/fortune-records/${fortune.id}`)
    ElMessage.success('删除算命记录成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除算命记录失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const handleDeleteLove = async (love) => {
  try {
    await ElMessageBox.confirm('确定删除这条爱情运势记录吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`${API_BASE}/admin/love-fortunes/${love.id}`)
    ElMessage.success('删除爱情运势记录成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除爱情运势失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const handleDeleteCategory = async (category) => {
  try {
    await ElMessageBox.confirm(`确定删除分类 "${category.name}" 吗？`, '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`${API_BASE}/admin/fortune-categories/${category.id}`)
    ElMessage.success('删除分类成功')
    await loadAllData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除分类失败: ' + (error.response?.data?.detail || error.message))
    }
  }
}
</script>

<style scoped>
.admin-container {
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

.el-card {
  margin-bottom: 20px;
}
</style>