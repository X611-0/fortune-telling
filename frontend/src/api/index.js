import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000, // 增加超时时间到30秒
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('=== 请求拦截器开始 ===')
    console.log('请求拦截器 - URL:', config.url)
    console.log('请求拦截器 - 方法:', config.method)
    
    // 检查是否为需要认证的API（排除登录、注册等公开接口）
    const publicEndpoints = ['auth/login', '/auth/login', 'auth/register', '/auth/register', 'auth/token', '/auth/token']
    const isPublicEndpoint = publicEndpoints.some(endpoint => {
      // 检查URL是否包含公开端点，不区分是否有前导斜杠
      const url = config.url || ''
      return url.includes(endpoint)
    })
    console.log('请求拦截器 - 是否为公开端点:', isPublicEndpoint)
    
    if (!isPublicEndpoint) {
      // 直接从localStorage获取token，避免在拦截器中使用store
      const token = localStorage.getItem('token')
      console.log('请求拦截器 - Token是否存在:', !!token)
      
      if (token) {
        // 增加token格式验证
        const tokenValid = token.includes('.') && token.split('.').length === 3
        console.log('请求拦截器 - Token格式是否有效:', tokenValid)
        console.log('请求拦截器 - Token值（前20位）:', token.substring(0, 20) + '...')
        
        if (tokenValid) {
          // 确保headers对象存在
          if (!config.headers) {
            config.headers = {}
          }
          
          // 设置Authorization头 - 使用Object.assign确保正确设置
          config.headers = Object.assign({}, config.headers, {
            'Authorization': `Bearer ${token.trim()}`  // 确保去除可能的空格
          })
          
          console.log('请求拦截器 - 已添加Authorization头')
          console.log('请求拦截器 - Authorization头:', `Bearer ${token.substring(0, 20)}...`)
          
          // 验证headers是否真的被设置
          console.log('请求拦截器 - 最终headers中的Authorization:', config.headers.Authorization ? `Bearer ${config.headers.Authorization.substring(7, 27)}...` : '未设置')
          
          // 额外验证：检查headers对象结构
          console.log('请求拦截器 - headers对象类型:', typeof config.headers)
          console.log('请求拦截器 - headers对象键:', Object.keys(config.headers))
        } else {
          console.log('请求拦截器 - Token格式无效，不添加Authorization头')
        }
      } else {
        console.log('请求拦截器 - 无token，未添加Authorization头')
        // 如果无token且不是公开接口，记录警告
        console.warn('请求拦截器 - 警告: 需要认证的接口但无token')
      }
    } else {
      console.log('请求拦截器 - 公开接口，跳过token验证')
    }
    console.log('=== 请求拦截器结束 ===')
    return config
  },
  (error) => {
    console.error('=== 请求拦截器错误 ===')
    console.error('请求拦截器错误:', error)
    // 捕获请求配置错误，确保错误信息完整
    if (error.config) {
      console.error('请求配置:', error.config.url, error.config.method)
    }
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('响应拦截器 - 成功:', response.config.url, response.status)
    return response
  },
  (error) => {
    console.error('响应拦截器 - 错误:', error.config?.url)
    
    // 更详细的错误类型检查
    if (error.response) {
      // 服务器响应了，但状态码不是2xx
      console.error('响应错误 - 状态码:', error.response.status)
      console.error('响应错误 - 数据:', error.response.data)
      
      if (error.response.status === 401) {
        console.log('响应拦截器 - 401错误，清除token并跳转到登录页')
        localStorage.removeItem('token')
        window.location.href = '/login'
      } else if (error.response.status === 403) {
        console.log('响应拦截器 - 403错误:', error.response.data)
      }
    } else if (error.request) {
      // 请求已发送，但没有收到响应
      console.error('请求错误 - 网络问题:', error.request)
      console.error('错误类型:', error.message)
    } else {
      // 请求配置出错
      console.error('请求配置错误:', error.message)
    }
    
    return Promise.reject(error)
  }
)

export default api