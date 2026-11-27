<template>
  <div v-if="series.length > 0" class="space-y-4 text-sm text-gray-700">
    <!-- KPI Summary Grid -->
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
      <div class="rounded-md border border-gray-200 bg-gray-50/70 p-3">
        <p class="text-xs font-medium text-gray-500">Period</p>
        <p class="mt-1 text-base font-semibold text-gray-900 tabular-nums">
          {{ firstYear }} – {{ lastYear }}
        </p>
        <p class="text-xs text-gray-500">
          {{ spanYears }} {{ spanYears === 1 ? 'year' : 'years' }}
        </p>
      </div>

      <div class="rounded-md border border-gray-200 bg-gray-50/70 p-3">
        <p class="text-xs font-medium text-gray-500">Cumulative Change</p>
        <p
          class="mt-1 text-base font-semibold tabular-nums"
          :class="changePct >= 0 ? 'text-blue-600' : 'text-emerald-700'"
        >
          {{ formatSignedPct(changePct) }}
        </p>
      </div>

      <div class="col-span-2 sm:col-span-1 rounded-md border border-gray-200 bg-gray-50/70 p-3">
        <p class="text-xs font-medium text-gray-500">Avg. Annual Rate</p>
        <p class="mt-1 text-base font-semibold text-gray-900 tabular-nums">
          {{ cagr !== null ? `${formatSignedPct(cagr)} / yr` : '—' }}
        </p>
      </div>
    </div>

    <!-- Year-by-Year Progression Chart -->
    <inflation-line-chart
      :points="series"
      :year1="year1"
      :year2="year2"
      metric-label="Inflation"
      metric-format="pct"
    ></inflation-line-chart>

    <!-- Scrollable Year-by-Year Table -->
    <div class="max-h-60 overflow-y-auto rounded-md border border-gray-200">
      <table class="w-full text-left border-collapse">
        <thead class="sticky top-0 bg-gray-50 border-b border-gray-200 text-xs font-semibold uppercase tracking-wider text-gray-500">
          <tr>
            <th class="py-2 px-3">Year</th>
            <th class="py-2 px-3 text-right">Inflation</th>
            <th class="py-2 px-3 text-right">Equivalent Value</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 text-sm">
          <tr
            v-for="row in series"
            :key="row.year"
            class="hover:bg-blue-50/40 transition-colors"
            :class="row.year === year1 || row.year === year2 ? 'bg-blue-50/30 font-medium' : ''"
          >
            <td class="py-2 px-3 text-gray-900 tabular-nums">{{ row.year }}</td>
            <td
              class="py-2 px-3 text-right tabular-nums"
              :class="
                row.metric !== undefined && row.metric < 0
                  ? 'text-emerald-700'
                  : 'text-gray-600'
              "
            >
              {{ row.metric !== undefined ? formatSignedPct(row.metric) : '—' }}
            </td>
            <td class="py-2 px-3 text-right text-gray-900 tabular-nums">
              RM {{ formatRm(row.value) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div v-else class="py-4 text-center text-sm text-gray-500">
    No data available for the selected year range.
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import InflationLineChart from './InflationLineChart.vue'
import { getGeneralInflationSeries } from '@/services/inflationService'
import { calculatorState } from '@/state/calculatorState'

const { year1, year2, value1 } = calculatorState

const series = computed(() =>
  getGeneralInflationSeries(year1.value, year2.value, value1.value)
)

const firstYear = computed(() => series.value[0]?.year ?? year1.value)
const lastYear = computed(
  () => series.value[series.value.length - 1]?.year ?? year2.value
)
const spanYears = computed(() => Math.abs(year2.value - year1.value))

const endpointValues = computed(() => {
  const pts = series.value
  if (pts.length === 0) return { v1: 0, v2: 0 }
  const first = pts[0].value
  const last = pts[pts.length - 1].value
  return year2.value >= year1.value
    ? { v1: first, v2: last }
    : { v1: last, v2: first }
})

const changePct = computed(() => {
  const { v1, v2 } = endpointValues.value
  if (v1 === 0) return 0
  return (v2 / v1 - 1) * 100
})

const cagr = computed(() => {
  const { v1, v2 } = endpointValues.value
  if (spanYears.value < 1 || v1 <= 0 || v2 <= 0) return null
  return (Math.pow(v2 / v1, 1 / spanYears.value) - 1) * 100
})

const formatSignedPct = (pct: number): string => {
  const sign = pct > 0 ? '+' : ''
  return `${sign}${pct.toFixed(2)}%`
}

const formatRm = (val: number): string =>
  val.toLocaleString('en-MY', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
</script>
