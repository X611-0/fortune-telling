import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token'))
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const isAuthenticated = ref(!!token.value)

  const login = async (username, password) => {
    try {
      console.log('登录 - 开始', { username })
      const response = await api.post('/auth/login', { username, password })
      const { access_token } = response.data
      console.log('登录 - 成功获取token', access_token ? `${access_token.substring(0, 10)}...` : '无token')
      
      token.value = access_token
      isAuthenticated.value = true
      localStorage.setItem('token', access_token)
      console.log('登录 - token已保存到localStorage', !!localStorage.getItem('token'))
      console.log('登录 - 认证状态更新为', isAuthenticated.value)
      
      // 获取用户信息
      await getUserProfile()
      console.log('登录 - 用户信息获取完成')
      
      return { success: true }
    } catch (error) {
      console.error('登录 - 失败:', error.response?.status, error.response?.data)
      return { success: false, message: error.response?.data?.detail || '登录失败' }
    }
  }

  const register = async (userData) => {
    try {
      await api.post('/auth/register', userData)
      return { success: true }
    } catch (error) {
      return { success: false, message: error.response?.data?.detail || '注册失败' }
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    isAuthenticated.value = false
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const getUserProfile = async () => {
    try {
      const response = await api.get('/user/profile')
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    getUserProfile
  }
})