import App from './App.vue'
import { createApp } from 'vue'
import { useMatomoto } from './configuration/useMatamoto'
import { router } from './router'
import { setupWatch } from './state/routeState'

import './assets/index.scss'

const app = createApp(App)

app.use(router)
useMatomoto(app, router)

app.mount('#app')

router.isReady().then(() => {
  setupWatch()
})
