/**
 * 股票系统 - 主JavaScript文件
 */

// 创建Vue应用
const { createApp, ref, computed, onMounted, onUnmounted } = Vue;

// 全局配置
const globalConfig = {
    apiBaseUrl: '/api',
    socketUrl: window.location.origin,
    currentYear: new Date().getFullYear()
};

// 创建Vue应用主实例
const app = createApp({
    setup() {
        // 提供全局状态和方法
        const loading = ref(false);
        const serverError = ref(null);
        
        // 开始加载状态
        const startLoading = () => {
            loading.value = true;
        };
        
        // 结束加载状态
        const stopLoading = () => {
            loading.value = false;
        };
        
        // 设置服务器错误
        const setServerError = (error) => {
            serverError.value = error;
            console.error('Server error:', error);
        };
        
        // 清除服务器错误
        const clearServerError = () => {
            serverError.value = null;
        };
        
        // 格式化数字为金额
        const formatCurrency = (value) => {
            if (typeof value !== 'number') {
                return '0.00';
            }
            return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        };
        
        // 格式化百分比
        const formatPercent = (value) => {
            if (typeof value !== 'number') {
                return '0.00%';
            }
            return (value * 100).toFixed(2) + '%';
        };
        
        // 格式化日期
        const formatDate = (dateString) => {
            const date = new Date(dateString);
            return date.toLocaleDateString('zh-CN');
        };
        
        // 格式化时间
        const formatTime = (dateString) => {
            const date = new Date(dateString);
            return date.toLocaleTimeString('zh-CN');
        };
        
        // 格式化日期时间
        const formatDateTime = (dateString) => {
            const date = new Date(dateString);
            return date.toLocaleString('zh-CN');
        };
        
        // 添加当前年份供模板使用
        const now = {
            year: globalConfig.currentYear
        };
        
        // 暴露给模板使用的属性和方法
        return {
            loading,
            serverError,
            startLoading,
            stopLoading,
            setServerError,
            clearServerError,
            formatCurrency,
            formatPercent,
            formatDate,
            formatTime,
            formatDateTime,
            now
        };
    }
});

// 配置axios全局拦截器
axios.interceptors.request.use(
    (config) => {
        // 在发送请求前做些什么
        app.config.globalProperties.startLoading();
        return config;
    },
    (error) => {
        // 对请求错误做些什么
        app.config.globalProperties.stopLoading();
        return Promise.reject(error);
    }
);

axios.interceptors.response.use(
    (response) => {
        // 对响应数据做些什么
        app.config.globalProperties.stopLoading();
        return response;
    },
    (error) => {
        // 对响应错误做些什么
        app.config.globalProperties.stopLoading();
        app.config.globalProperties.setServerError(error);
        return Promise.reject(error);
    }
);

// 挂载Vue应用
app.use(ElementPlus).mount('#app'); 