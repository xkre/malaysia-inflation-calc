<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import Calculator from './components/Calculator.vue';
import DetailedInfo from './components/DetailedInfo.vue';
import DataSource from './components/DataSource.vue';
</script>

<template>
  <div class="app-container flex flex-col justify-between pt-8">
    <div class="flex flex-col">
      <h1 class="mb-6">Malaysia Inflation Calculator</h1>
      <calculator></calculator>
      <detailed-info></detailed-info>
    </div>

    <data-source></data-source>
  </div>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  

  @apply px-4;

  h1 {
    @apply text-xl;
  }

  .app-container {
    max-width: calc(100vw - 1rem);
    height: calc(100vh - 1rem);
  }
}
</style>
