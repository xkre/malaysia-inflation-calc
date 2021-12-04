import {  createRouter, createWebHistory, LocationAsPath, RouteLocationOptions, RouteQueryAndHash } from "vue-router"

export const router = createRouter({
  history: createWebHistory(),
  routes: [{
    path: '/',
    component: () => import('./components/Calculator.vue')
  }]
})
