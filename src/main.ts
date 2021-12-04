import { createApp } from 'vue'
import App from './App.vue'
import './assets/index.scss'

import { setupWatch } from './state/routeState'

const app = createApp(App)
app.mount('#app')

setupWatch()