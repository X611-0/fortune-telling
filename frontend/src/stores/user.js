import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'

export const useUserStore = defineStore('user', () => {
  const baziRecords = ref([])
  const fortuneRecords = ref([])
  
  // 测试token是否正确存储和可用的辅助函数
  const testToken = () => {
    console.log('=== Token测试 ===')
    const token = localStorage.getItem('token')
    console.log('Token是否存在:', !!token)
    console.log('Token长度:', token ? token.length : 0)
    console.log('Token值（前20位）:', token ? token.substring(0, 20) + '...' : '无')
    
    // 检查token格式
    if (token) {
      const hasDot = token.includes('.')
      console.log('Token包含分隔符(.):', hasDot)
      console.log('Token段数:', hasDot ? token.split('.').length : 0)
    }
    
    return { exists: !!token, length: token ? token.length : 0 }
  }
  
  // 测试Authorization头传递
  const testAuthHeader = async () => {
    try {
      console.log('=== 测试Authorization头传递 ===')
      const token = localStorage.getItem('token')
      console.log('使用的token:', token ? token.substring(0, 20) + '...' : '无')
      
      // 创建完整的axios实例，绕过拦截器，直接测试
      const axios = await import('axios')
      const testInstance = axios.default.create({
        baseURL: 'http://localhost:8000/api', // 使用完整URL，绕过代理
        timeout: 10000
      })
      
      // 显式设置Authorization头
      const headers = {
        'Authorization': `Bearer ${token?.trim()}`
      }
      console.log('请求头:', headers)
      console.log('完整请求URL:', 'http://localhost:8000/api/bazi/test-auth-header')
      
      // 直接发送请求，不经过API拦截器
      const response = await testInstance.get('/bazi/test-auth-header', { headers })
      console.log('测试结果:', response.data)
      return response.data
    } catch (error) {
      console.error('Authorization头测试失败:', error.response || error)
      return { success: false, error: error.response?.data || error.message }
    }
  }

  const getBaziRecords = async () => {
    try {
      const authStore = useAuthStore()
      // 直接从localStorage获取token
      const localStorageToken = localStorage.getItem('token')
      
      console.log('当前用户认证状态:', authStore.isAuthenticated)
      console.log('localStorage中的Token是否存在:', !!localStorageToken)
      
      // 先检查认证状态
      if (!localStorageToken || !authStore.isAuthenticated) {
        console.error('未认证或token缺失，无法获取八字记录')
        return
      }
      
      // 创建完整的axios实例，绕过拦截器，直接发送请求
      const axios = await import('axios')
      const directInstance = axios.default.create({
        baseURL: 'http://localhost:8000/api', // 使用完整URL，绕过代理
        timeout: 30000
      })
      
      // 显式设置Authorization头
      const headers = {
        'Authorization': `Bearer ${localStorageToken.trim()}`
      }
      console.log('显式设置Authorization头:', headers.Authorization)
      console.log('完整请求URL:', 'http://localhost:8000/api/bazi')
      
      const response = await directInstance.get('/bazi', { headers })
      baziRecords.value = response.data
      console.log('获取八字记录成功，共', response.data.length, '条记录')
    } catch (error) {
      console.error('获取八字记录失败:', error)
      
      // 改进错误详情显示
      if (error.response) {
        // 服务器响应了错误状态码
        console.error('错误详情:', error.response.status, error.response.data)
      } else if (error.request) {
        // 网络错误
        console.error('网络错误详情:', error.message, error.request)
      } else {
        // 其他错误
        console.error('错误详情:', error.message)
      }
    }
  }

  // 数据转换函数
  const convertYearToIndex = (yearStr) => {
    // 年柱格式如 "甲子1", "甲子2", ... "甲子60"
    const match = yearStr.match(/甲子(\d+)/)
    return match ? parseInt(match[1]) : 1
  }
  
  const convertMonthToIndex = (monthStr) => {
    const months = ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月']
    return months.indexOf(monthStr) + 1
  }
  
  const convertDayToIndex = (dayStr) => {
    // 日柱格式如 "初1", "初2", ... "初30"
    const match = dayStr.match(/初(\d+)/)
    return match ? parseInt(match[1]) : 1
  }
  
  const convertHourToIndex = (hourStr) => {
    const hours = ['子时', '丑时', '寅时', '卯时', '辰时', '巳时', '午时', '未时', '申时', '酉时', '戌时', '亥时']
    return hours.indexOf(hourStr) + 1
  }

  const createBaziRecord = async (baziData, retryCount = 0, maxRetries = 2) => {
    try {
      const authStore = useAuthStore()
      // 直接从localStorage获取token
      const localStorageToken = localStorage.getItem('token')
      
      console.log('当前用户认证状态:', authStore.isAuthenticated)
      console.log('authStore中的Token是否存在:', !!authStore.token)
      console.log('authStore中的Token值（前20位）:', authStore.token ? authStore.token.substring(0, 20) + '...' : '无')
      console.log('localStorage中的Token是否存在:', !!localStorageToken)
      console.log('localStorage中的Token值（前20位）:', localStorageToken ? localStorageToken.substring(0, 20) + '...' : '无')
      
      // 先检查认证状态
      if (!localStorageToken || !authStore.isAuthenticated) {
        console.error('未认证或token缺失，无法创建八字记录')
        return { success: false, message: '请先登录' }
      }
      
      // 如果authStore中的token与localStorage不同步，进行同步
      if (authStore.token !== localStorageToken) {
        console.log('检测到token不同步，更新authStore中的token')
        authStore.token = localStorageToken
        authStore.isAuthenticated = true
      }
      
      // 额外验证token格式
      console.log('Token格式验证 - 包含分隔符(.):', localStorageToken.includes('.'))
      console.log('Token格式验证 - 段数:', localStorageToken.split('.').length)
      console.log('Token格式验证 - 长度:', localStorageToken.length)
      
      // 转换数据格式：将八字字符串转换为后端期望的整数索引
      const processedData = {
        year: convertYearToIndex(baziData.year),
        month: convertMonthToIndex(baziData.month),
        day: convertDayToIndex(baziData.day),
        hour: convertHourToIndex(baziData.hour),
        gender: baziData.gender
      }
      
      console.log('原始八字数据:', baziData)
      console.log('转换后的请求数据:', processedData)
      console.log(`发起请求 - 第${retryCount + 1}次尝试`)
      
      // 创建完整的axios实例，绕过拦截器，直接发送请求
      const axios = await import('axios')
      const directInstance = axios.default.create({
        baseURL: 'http://localhost:8000/api', // 使用完整URL，绕过代理
        timeout: 30000
      })
      
      // 显式设置Authorization头
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorageToken.trim()}`
      }
      console.log('显式设置Authorization头:', headers.Authorization)
      console.log('完整请求URL:', 'http://localhost:8000/api/bazi')
      
      const startTime = Date.now()
      // 直接发送请求，不经过API拦截器
      const response = await directInstance.post('/bazi', processedData, { headers })
      const endTime = Date.now()
      
      console.log(`请求完成，耗时: ${endTime - startTime}ms`)
      console.log('响应状态:', response.status)
      console.log('响应数据:', response.data)
      
      // 刷新记录列表
      await getBaziRecords()
      console.log('创建八字记录成功')
      return { success: true, data: response.data }
    } catch (error) {
      console.error('创建八字记录失败:', error)
      
      // 改进错误信息处理
      let errorMessage = '创建失败'
      
      if (error.response) {
        // 服务器响应了错误状态码
        console.error('完整错误响应:', error.response)
        
        // 422错误：数据校验失败
        if (error.response.status === 422) {
          const validationErrors = error.response.data?.detail || []
          console.error('数据校验错误详情:', validationErrors)
          
          // 提取具体的错误信息
          if (Array.isArray(validationErrors)) {
            const errorMessages = validationErrors.map(err => {
              return `${err.loc?.join('.')}: ${err.msg}`
            }).join('; ')
            errorMessage = `数据格式错误: ${errorMessages}`
          } else {
            errorMessage = `数据校验失败: ${JSON.stringify(validationErrors)}`
          }
        } else {
          errorMessage = error.response.data?.detail || error.response.statusText || errorMessage
        }
        
        console.error('错误详情:', error.response.status, error.response.data)
      } else if (error.request) {
        // 网络错误，包括超时
        errorMessage = `网络错误: ${error.message}`
        console.error('网络错误详情:', error.message)
        
        // 对于超时错误，添加重试逻辑
        if (error.code === 'ECONNABORTED' && retryCount < maxRetries) {
          console.log(`请求超时，准备第${retryCount + 2}次重试...`)
          // 指数退避重试
          const delay = 1000 * Math.pow(2, retryCount)
          await new Promise(resolve => setTimeout(resolve, delay))
          return createBaziRecord(baziData, retryCount + 1, maxRetries)
        }
      } else {
        // 其他错误
        errorMessage = error.message || errorMessage
        console.error('错误详情:', error.message)
      }
      
      return { success: false, message: errorMessage }
    }
  }

  const getFortuneRecords = async () => {
    try {
      const authStore = useAuthStore()
      console.log('当前用户认证状态:', authStore.isAuthenticated)
      console.log('请求路径: fortune/records')
      const response = await api.get('fortune/records')
      // 后端返回的是 {records: [...]} 格式，需要提取records数组
      fortuneRecords.value = response.data.records || []
      console.log('获取算命记录成功，共', fortuneRecords.value.length, '条记录')
    } catch (error) {
      console.error('获取算命记录失败:', error)
      console.error('错误详情:', error.response?.status, error.response?.data)
      // 出错时设置为空数组，避免.filter()方法报错
      fortuneRecords.value = []
    }
  }

  const calculateFortune = async (fortuneData) => {
    try {
      const authStore = useAuthStore()
      // 直接从localStorage获取token
      const localStorageToken = localStorage.getItem('token')
      
      console.log('当前用户认证状态:', authStore.isAuthenticated)
      console.log('localStorage中的Token是否存在:', !!localStorageToken)
      console.log('计算运势，请求数据:', fortuneData)
      
      // 先检查认证状态
      if (!localStorageToken || !authStore.isAuthenticated) {
        console.error('未认证或token缺失，无法计算运势')
        return { success: false, message: '请先登录' }
      }
      
      // 创建完整的axios实例，绕过拦截器，直接发送请求
      const axios = await import('axios')
      const directInstance = axios.default.create({
        baseURL: 'http://localhost:8000/api', // 使用完整URL，绕过代理
        timeout: 30000
      })
      
      // 显式设置Authorization头
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorageToken.trim()}`
      }
      console.log('显式设置Authorization头:', headers.Authorization)
      console.log('完整请求URL:', 'http://localhost:8000/api/fortune')
      
      const response = await directInstance.post('/fortune', fortuneData, { headers })
      await getFortuneRecords()
      console.log('计算运势成功')
      return { success: true, data: response.data }
    } catch (error) {
      console.error('计算运势失败:', error)
      
      // 改进错误信息处理
      let errorMessage = '算命失败'
      
      if (error.response) {
        // 服务器响应了错误状态码
        console.error('完整错误响应:', error.response)
        
        // 422错误：数据校验失败
        if (error.response.status === 422) {
          const validationErrors = error.response.data?.detail || []
          console.error('数据校验错误详情:', validationErrors)
          
          // 提取具体的错误信息
          if (Array.isArray(validationErrors)) {
            const errorMessages = validationErrors.map(err => {
              return `${err.loc?.join('.')}: ${err.msg}`
            }).join('; ')
            errorMessage = `数据格式错误: ${errorMessages}`
          } else {
            errorMessage = `数据校验失败: ${JSON.stringify(validationErrors)}`
          }
        } else {
          errorMessage = error.response.data?.detail || error.response.statusText || errorMessage
        }
        
        console.error('错误详情:', error.response.status, error.response.data)
      } else if (error.request) {
        // 网络错误，包括超时
        errorMessage = `网络错误: ${error.message}`
        console.error('网络错误详情:', error.message)
      } else {
        // 其他错误
        errorMessage = error.message || errorMessage
        console.error('错误详情:', error.message)
      }
      
      return { success: false, message: errorMessage }
    }
  }

  const calculateLoveFortune = async (fortuneData) => {
    try {
      const authStore = useAuthStore()
      // 直接从localStorage获取token
      const localStorageToken = localStorage.getItem('token')
      
      console.log('当前用户认证状态:', authStore.isAuthenticated)
      console.log('localStorage中的Token是否存在:', !!localStorageToken)
      console.log('计算爱情运势，请求数据:', fortuneData)
      
      // 先检查认证状态
      if (!localStorageToken || !authStore.isAuthenticated) {
        console.error('未认证或token缺失，无法计算爱情运势')
        return { success: false, message: '请先登录' }
      }
      
      // 创建完整的axios实例，绕过拦截器，直接发送请求
      const axios = await import('axios')
      const directInstance = axios.default.create({
        baseURL: 'http://localhost:8000/api', // 使用完整URL，绕过代理
        timeout: 30000
      })
      
      // 显式设置Authorization头
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorageToken.trim()}`
      }
      console.log('显式设置Authorization头:', headers.Authorization)
      console.log('完整请求URL:', 'http://localhost:8000/api/fortune/love')
      
      const response = await directInstance.post('/fortune/love', fortuneData, { headers })
      console.log('计算爱情运势成功')
      return { success: true, data: response.data }
    } catch (error) {
      console.error('计算爱情运势失败:', error)
      
      // 改进错误信息处理
      let errorMessage = '爱情运势计算失败'
      
      if (error.response) {
        // 服务器响应了错误状态码
        console.error('完整错误响应:', error.response)
        
        // 422错误：数据校验失败
        if (error.response.status === 422) {
          const validationErrors = error.response.data?.detail || []
          console.error('数据校验错误详情:', validationErrors)
          
          // 提取具体的错误信息
          if (Array.isArray(validationErrors)) {
            const errorMessages = validationErrors.map(err => {
              return `${err.loc?.join('.')}: ${err.msg}`
            }).join('; ')
            errorMessage = `数据格式错误: ${errorMessages}`
          } else {
            errorMessage = `数据校验失败: ${JSON.stringify(validationErrors)}`
          }
        } else {
          errorMessage = error.response.data?.detail || error.response.statusText || errorMessage
        }
        
        console.error('错误详情:', error.response.status, error.response.data)
      } else if (error.request) {
        // 网络错误，包括超时
        errorMessage = `网络错误: ${error.message}`
        console.error('网络错误详情:', error.message)
      } else {
        // 其他错误
        errorMessage = error.message || errorMessage
        console.error('错误详情:', error.message)
      }
      
      return { success: false, message: errorMessage }
    }
  }

  const getLoveFortuneRecords = async () => {
    try {
      const authStore = useAuthStore()
      console.log('当前用户认证状态:', authStore.isAuthenticated)
      console.log('请求路径: fortune/love/records')
      const response = await api.get('fortune/love/records')
      // 将爱情运势记录合并到总的运势记录中
      if (response.data && response.data.records) {
        const loveRecords = response.data.records
        // 获取现有的运势记录
        await getFortuneRecords()
        // 合并记录（避免重复）
        const existingIds = new Set(fortuneRecords.value.map(record => record.id))
        const newRecords = loveRecords.filter(record => !existingIds.has(record.id))
        fortuneRecords.value = [...fortuneRecords.value, ...newRecords]
        console.log('获取爱情运势记录成功，合并后共', fortuneRecords.value.length, '条记录')
      }
      return response.data
    } catch (error) {
      console.error('获取爱情运势记录失败:', error)
      console.error('错误详情:', error.response?.status, error.response?.data)
      return []
    }
  }

  return {
    baziRecords,
    fortuneRecords,
    getBaziRecords,
    createBaziRecord,
    getFortuneRecords,
    calculateFortune,
    calculateLoveFortune,
    getLoveFortuneRecords
  }
})