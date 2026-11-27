<template>
  <div>
    <detailed-calculator></detailed-calculator>
    <detailed-info mode="detailed"></detailed-info>
  </div>
</template>

<script setup lang="ts">
import { onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import DetailedCalculator from '@/components/Detailed/DetailedCalculator.vue'
import DetailedInfo from '@/components/DetailedInfo.vue'
import {
  hydrateDetailedStateFromQuery,
  setupDetailedRouteWatch,
} from '@/state/detailedCalculatorState'

const route = useRoute()
if (Object.keys(route.query).length > 0) {
  hydrateDetailedStateFromQuery(route.query)
}

const stopWatch = setupDetailedRouteWatch()
onUnmounted(() => {
  stopWatch()
})
</script>
