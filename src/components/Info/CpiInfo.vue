<template>
  <div>
    <div v-if="cpiData.year1">
      {{ year1 }} CPI: {{ cpiData.year1 }}
    </div>
    <div v-else>
      No data
    </div>
    <div v-if="cpiData.year2">
      {{ year2 }} CPI: {{ cpiData.year2 }}
    </div>
    <div v-else>
      No data
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from '@vue/reactivity'
import { getCPI } from '../../services/inflationService'
import { calculatorState } from '../../state/calculatorState'

const { year1, year2, inflationType, part } = calculatorState

const cpiData = computed(() => {
  const cpi = getCPI(year1.value, year2.value, inflationType.value, part.value)

  return cpi
})
</script>
