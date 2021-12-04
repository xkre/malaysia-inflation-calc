import { createMemoryHistory, createRouter, createWebHistory, useRouter } from "vue-router";

export const router = createRouter({
  history: createWebHistory(),
  routes: [{
    path: '/',
    component: () => import('./components/Calculator.vue')
  }]
})