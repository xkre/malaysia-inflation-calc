<template>
  <div class="h-screen flex flex-col">
    <main-header></main-header>
    <div class="container mx-auto px-4 md:px-0">
      <div class="max-w-screen-sm mx-auto">
        <section-tabs></section-tabs>
        <router-view></router-view>
      </div>
    </div>

    <data-source></data-source>
    <reload-prompt></reload-prompt>
  </div>
</template>

<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import SectionTabs from './components/SectionTabs.vue';
import DataSource from './components/DataSource.vue';
import MainHeader from './components/MainHeader.vue';
import ReloadPrompt from './components/ReloadPrompt.vue';
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
