import App from './App.vue'
import { createApp } from 'vue'
import { useMatomoto } from './configuration/useMatamoto'
import { router } from './router'
import { setupWatch } from './state/routeState'
import { registerSW } from 'virtual:pwa-register'

import './assets/index.scss'

const app = createApp(App)

useMatomoto(app, router)

app.mount('#app')

setupWatch()

registerSW({
  onNeedRefresh() {},
  onOfflineReady() {},
})
