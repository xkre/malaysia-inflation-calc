<template>
  <div v-if="hasValidData" class="space-y-4 text-sm text-gray-700">
    <!-- KPI Summary Grid -->
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
      <div class="rounded-md border border-gray-200 bg-gray-50/70 p-3">
        <p class="text-xs font-medium text-gray-500">
          {{ year1 }} {{ description }}
        </p>
        <p class="mt-1 text-base font-semibold text-gray-900 tabular-nums">
          {{ formatMetric(cpiData.year1!) }}
        </p>
      </div>

      <div class="rounded-md border border-gray-200 bg-gray-50/70 p-3">
        <p class="text-xs font-medium text-gray-500">
          {{ year2 }} {{ description }}
        </p>
        <p class="mt-1 text-base font-semibold text-gray-900 tabular-nums">
          {{ formatMetric(cpiData.year2!) }}
        </p>
      </div>

      <div class="col-span-2 sm:col-span-1 rounded-md border border-gray-200 bg-gray-50/70 p-3">
        <p class="text-xs font-medium text-gray-500">Total Change</p>
        <p
          class="mt-1 text-base font-semibold tabular-nums"
          :class="changePct >= 0 ? 'text-blue-600' : 'text-emerald-700'"
        >
          {{ formatSignedPct(changePct) }}
        </p>
        <p v-if="cagr !== null" class="text-xs text-gray-500 tabular-nums">
          {{ formatSignedPct(cagr) }} / yr
        </p>
      </div>
    </div>

    <!-- Year-by-Year Progression Chart -->
    <inflation-line-chart
      :points="series"
      :year1="year1"
      :year2="year2"
      :metric-label="chartMetricLabel"
      :metric-format="chartMetricFormat"
    ></inflation-line-chart>
  </div>

  <div v-else class="py-4 text-center text-sm text-gray-500">
    No data available for the selected year range.
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import InflationLineChart from './InflationLineChart.vue'
import { getCPI, getCPISeries } from '@/services/inflationService'
import { calculatorState } from '@/state/calculatorState'
import { InflationType } from '@/types/InflatitonTypeEnum'

const { year1, year2, value1, inflationType, part } = calculatorState

const cpiData = computed(() =>
  getCPI(year1.value, year2.value, inflationType.value, part.value)
)

const hasValidData = computed(
  () =>
    cpiData.value.year1 !== undefined &&
    cpiData.value.year2 !== undefined &&
    cpiData.value.year1 !== 0
)

const series = computed(() =>
  getCPISeries(
    year1.value,
    year2.value,
    value1.value,
    inflationType.value,
    part.value
  )
)

const description = computed(() =>
  inflationType.value === InflationType.BigMac ? 'Big Mac Price' : 'CPI'
)

const chartMetricLabel = computed(() =>
  inflationType.value === InflationType.BigMac ? 'Big Mac' : 'CPI'
)

const chartMetricFormat = computed<'rm' | 'index'>(() =>
  inflationType.value === InflationType.BigMac ? 'rm' : 'index'
)

const changePct = computed(() => {
  if (!hasValidData.value) return 0
  return (cpiData.value.year2! / cpiData.value.year1! - 1) * 100
})

const spanYears = computed(() => Math.abs(year2.value - year1.value))

const cagr = computed(() => {
  if (!hasValidData.value || spanYears.value < 1) return null
  const ratio = cpiData.value.year2! / cpiData.value.year1!
  if (ratio <= 0) return null
  return (Math.pow(ratio, 1 / spanYears.value) - 1) * 100
})

const formatMetric = (val: number): string => {
  if (inflationType.value === InflationType.BigMac) {
    return `RM ${val.toFixed(2)}`
  }
  return String(val)
}

const formatSignedPct = (pct: number): string => {
  const sign = pct > 0 ? '+' : ''
  return `${sign}${pct.toFixed(2)}%`
}
</script>
