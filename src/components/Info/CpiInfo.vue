<template>
  <div>
    <div v-if="cpiData.year1" class="py-1">
      <span class="font-semibold">{{ year1 }}</span> {{ description }}: {{ cpiData.year1 }}
    </div>
    <div v-else>
      No data
    </div>
    <div v-if="cpiData.year2" class="py-1">
      <span class="font-semibold">{{ year2 }}</span> {{ description }}: {{ cpiData.year2 }}
    </div>
    <div v-else>
      No data
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from '@vue/reactivity'
import { getCPI } from '@/services/inflationService'
import { calculatorState } from '@/state/calculatorState'
import { InflationType } from '@/types/InflatitonTypeEnum';

const { year1, year2, inflationType, part } = calculatorState

const cpiData = computed(() => {
  const cpi = getCPI(year1.value, year2.value, inflationType.value, part.value)

  return cpi
})

const description = computed(() => {
  if (inflationType.value === InflationType.BigMac) {
    return 'Big Mac Price'
  }

  return 'CPI'
})
</script>
