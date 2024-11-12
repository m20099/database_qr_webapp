import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)  // `const`を追加して宣言
app.use(router)
app.mount('#app')
