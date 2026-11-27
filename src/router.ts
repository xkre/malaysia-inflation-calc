import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'simple',
      component: () => import('./views/SimpleCalculatorView.vue'),
    },
    {
      path: '/detailed',
      name: 'detailed',
      component: () => import('./views/DetailedCalculatorView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: { name: 'simple' },
    },
  ],
})
