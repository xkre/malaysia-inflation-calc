<template>
  <div class="space-y-4 text-sm text-gray-700">
    <!-- Category Summary -->
    <div v-if="activeNode" class="space-y-0.5">
      <div>
        <span class="font-semibold text-gray-900">
          {{ LEVEL_LABELS[activeNode.digits] }} · {{ activeNode.code }}:
        </span>
        {{ activeNode.descEn }}
      </div>
      <div v-if="hasDistinctBm" class="text-xs text-gray-500">
        {{ activeNode.descBm }}
      </div>
      <div v-if="breadcrumbText" class="text-xs text-gray-500">
        {{ breadcrumbText }}
      </div>
    </div>

    <!-- Loading Monthly State -->
    <div
      v-if="granularity === 'm' && monthlyLoading && !monthlyLoaded"
      class="py-4 text-center text-sm text-gray-500"
    >
      Loading monthly data...
    </div>

    <!-- Valid Data View -->
    <template v-else-if="lookup.cpi1 !== undefined && lookup.cpi2 !== undefined">
      <!-- KPI Summary Grid -->
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
        <div class="rounded-md border border-gray-200 bg-gray-50/70 p-3">
          <p class="text-xs font-medium text-gray-500">
            {{ period1ShortLabel }} CPI
          </p>
          <p class="mt-1 text-base font-semibold text-gray-900 tabular-nums">
            {{ formatIndex(lookup.cpi1) }}
          </p>
          <p v-if="period1Subtext" class="text-[11px] text-gray-400">
            {{ period1Subtext }}
          </p>
        </div>

        <div class="rounded-md border border-gray-200 bg-gray-50/70 p-3">
          <p class="text-xs font-medium text-gray-500">
            {{ period2ShortLabel }} CPI
          </p>
          <p class="mt-1 text-base font-semibold text-gray-900 tabular-nums">
            {{ formatIndex(lookup.cpi2) }}
          </p>
          <p v-if="period2Subtext" class="text-[11px] text-gray-400">
            {{ period2Subtext }}
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
          <p class="text-xs text-gray-500 tabular-nums">
            <template v-if="cagr !== null">
              {{ formatSignedPct(cagr) }} / yr · {{ shortSpanLabel }}
            </template>
            <template v-else>
              {{ shortSpanLabel }}
            </template>
          </p>
        </div>
      </div>

      <!-- Progression Line Chart -->
      <inflation-line-chart
        :points="chartPoints"
        :target-key="targetChartKey"
        metric-label="CPI"
        metric-format="index"
        :metric-decimals="granularity === 'm' ? 1 : 2"
      ></inflation-line-chart>

      <!-- Contextual Parent / Overall Benchmark -->
      <div
        v-if="benchmarkChangePct !== null"
        class="text-xs text-gray-500 pt-2 border-t border-gray-100"
      >
        Benchmark — {{ benchmark.label }}:
        <span class="font-medium text-gray-700">{{ formatSignedPct(benchmarkChangePct) }}</span>
        over the same period.
      </div>
    </template>

    <!-- No Data State -->
    <div v-else class="py-4 text-center text-sm text-gray-500">
      No data available for the selected period.
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import InflationLineChart from './InflationLineChart.vue'
import { detailedCalculatorState } from '@/state/detailedCalculatorState'
import {
  LEVEL_LABELS,
  MONTH_NAMES,
  calculateCAGR,
  formatMonthLabel,
  formatYearMonth,
  getAnnualCPI,
  getAnnualMeta,
  getBreadcrumb,
  getDetailedAnnualSeries,
  getDetailedMonthlySeries,
  getMonthlyCPI,
  getNodeByCode,
  getParentBenchmarkCode,
  monthlyLoaded,
  monthlyLoading,
} from '@/services/detailedInflationService'

const { granularity, selectedCode, year1, month1, year2, month2, value1 } =
  detailedCalculatorState

const meta = getAnnualMeta()
const activeNode = computed(() => getNodeByCode(selectedCode.value))
const breadcrumb = computed(() => getBreadcrumb(selectedCode.value))

const hasDistinctBm = computed(() => {
  const n = activeNode.value
  return Boolean(
    n && n.descBm.trim().toLowerCase() !== n.descEn.trim().toLowerCase()
  )
})

const breadcrumbText = computed(() => {
  const b = breadcrumb.value
  if (!b) return ''
  const parts = [
    `${b.division.code} ${b.division.descEn}`,
    `${b.group.code} ${b.group.descEn}`,
  ]
  if (b.classNode) parts.push(`${b.classNode.code} ${b.classNode.descEn}`)
  if (b.subclassNode) parts.push(`${b.subclassNode.code} ${b.subclassNode.descEn}`)
  return parts.join(' › ')
})

const ytdText = computed(() =>
  meta.ytdMonths < 12 ? `Jan–${MONTH_NAMES[meta.ytdMonths - 1]} YTD avg` : ''
)

const period1ShortLabel = computed(() =>
  granularity.value === 'm'
    ? formatMonthLabel(year1.value, month1.value)
    : String(year1.value)
)

const period2ShortLabel = computed(() =>
  granularity.value === 'm'
    ? formatMonthLabel(year2.value, month2.value)
    : String(year2.value)
)

const period1Subtext = computed(() =>
  granularity.value === 'y' && year1.value === meta.ytdYear ? ytdText.value : ''
)

const period2Subtext = computed(() =>
  granularity.value === 'y' && year2.value === meta.ytdYear ? ytdText.value : ''
)

const lookup = computed(() => {
  if (granularity.value === 'm') {
    return getMonthlyCPI(
      formatYearMonth(year1.value, month1.value),
      formatYearMonth(year2.value, month2.value),
      selectedCode.value
    )
  }
  return getAnnualCPI(year1.value, year2.value, selectedCode.value)
})

const chartPoints = computed(() => {
  if (granularity.value === 'm') {
    return getDetailedMonthlySeries(
      formatYearMonth(year1.value, month1.value),
      formatYearMonth(year2.value, month2.value),
      value1.value,
      selectedCode.value
    )
  }
  return getDetailedAnnualSeries(
    year1.value,
    year2.value,
    value1.value,
    selectedCode.value
  )
})

const targetChartKey = computed<string | number>(() =>
  granularity.value === 'm'
    ? formatYearMonth(year2.value, month2.value)
    : year2.value
)

const spanYears = computed(() => {
  if (granularity.value === 'm') {
    const months = Math.abs(
      year2.value * 12 + month2.value - (year1.value * 12 + month1.value)
    )
    return months / 12
  }
  return Math.abs(year2.value - year1.value)
})

const shortSpanLabel = computed(() => {
  if (granularity.value === 'm') {
    const totalMonths = Math.abs(
      year2.value * 12 + month2.value - (year1.value * 12 + month1.value)
    )
    const yrs = Math.floor(totalMonths / 12)
    const remMonths = totalMonths % 12
    if (yrs === 0) return `${remMonths} ${remMonths === 1 ? 'mo' : 'mos'}`
    if (remMonths === 0) return `${yrs} ${yrs === 1 ? 'yr' : 'yrs'}`
    return `${yrs}y ${remMonths}m`
  }
  const yrs = Math.abs(year2.value - year1.value)
  return `${yrs} ${yrs === 1 ? 'yr' : 'yrs'}`
})

const changePct = computed(() => {
  const { cpi1, cpi2 } = lookup.value
  if (cpi1 === undefined || cpi2 === undefined || cpi1 === 0) return 0
  return (cpi2 / cpi1 - 1) * 100
})

const cagr = computed(() => {
  const { cpi1, cpi2 } = lookup.value
  if (cpi1 === undefined || cpi2 === undefined) return null
  return calculateCAGR(cpi1, cpi2, spanYears.value)
})

const benchmark = computed(() => getParentBenchmarkCode(selectedCode.value))

const benchmarkChangePct = computed(() => {
  const bCode = benchmark.value.code
  const res =
    granularity.value === 'm'
      ? getMonthlyCPI(
          formatYearMonth(year1.value, month1.value),
          formatYearMonth(year2.value, month2.value),
          bCode
        )
      : getAnnualCPI(year1.value, year2.value, bCode)

  if (res.cpi1 === undefined || res.cpi2 === undefined || res.cpi1 === 0) {
    return null
  }
  return (res.cpi2 / res.cpi1 - 1) * 100
})

const formatIndex = (val: number): string =>
  granularity.value === 'm' ? val.toFixed(1) : val.toFixed(2)

const formatSignedPct = (pct: number): string => {
  const sign = pct > 0 ? '+' : ''
  return `${sign}${pct.toFixed(2)}%`
}
</script>
