<template>
  <nav aria-label="Calculator sections" class="bg-gray-100 p-1 rounded-lg grid grid-cols-3 gap-1 mb-7">
    <router-link
      :to="{ name: 'simple' }"
      @click="trackSection('Simple')"
      class="text-center py-2 px-3 rounded-md text-sm font-medium transition-colors !no-underline hover:!no-underline flex items-center justify-center"
      :class="
        route.name === 'simple'
          ? 'bg-white !text-blue-600 shadow-sm'
          : '!text-gray-600 hover:!text-gray-900'
      "
    >
      Simple
    </router-link>

    <router-link
      :to="{ name: 'detailed' }"
      @click="trackSection('Detailed')"
      class="text-center py-2 px-3 rounded-md text-sm font-medium transition-colors !no-underline hover:!no-underline flex items-center justify-center"
      :class="
        route.name === 'detailed'
          ? 'bg-white !text-blue-600 shadow-sm'
          : '!text-gray-600 hover:!text-gray-900'
      "
    >
      Detailed
    </router-link>

    <button
      type="button"
      disabled
      aria-disabled="true"
      title="Advanced calculator coming soon"
      class="text-center py-2 px-2 sm:px-3 rounded-md text-sm font-medium text-gray-400 cursor-not-allowed flex items-center justify-center space-x-1.5 select-none"
    >
      <span>Advanced</span>
      <span class="text-[11px] font-medium px-1.5 py-0.5 rounded-full bg-gray-200 text-gray-500 leading-none">
        Soon
      </span>
    </button>
  </nav>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { trackEvent } from '@/helpers/matomo'

const route = useRoute()

const trackSection = (section: string) => {
  trackEvent('Navigation', 'Switch Section', section)
}
</script>
