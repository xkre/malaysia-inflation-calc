<template>
  <div>
    <mcoicop-picker></mcoicop-picker>

    <!-- Period Granularity Toggle -->
    <div class="flex items-center justify-between mb-6">
      <span class="font-medium text-gray-700">Period Mode</span>
      <div class="inline-flex rounded-md shadow-sm" role="group" aria-label="Period granularity">
        <button
          type="button"
          @click="setGranularity('y')"
          class="border py-1.5 px-3.5 text-sm font-medium rounded-l-md transition-colors"
          :class="
            granularity === 'y'
              ? 'border-blue-500 bg-blue-50 text-blue-600 z-10'
              : 'border-gray-300 bg-white text-gray-600 hover:border-blue-500 hover:bg-blue-50'
          "
        >
          Yearly (Avg)
        </button>
        <button
          type="button"
          @click="setGranularity('m')"
          class="-ml-px border py-1.5 px-3.5 text-sm font-medium rounded-r-md transition-colors"
          :class="
            granularity === 'm'
              ? 'border-blue-500 bg-blue-50 text-blue-600 z-10'
              : 'border-gray-300 bg-white text-gray-600 hover:border-blue-500 hover:bg-blue-50'
          "
        >
          Monthly
        </button>
      </div>
    </div>

    <!-- Value & Start Period Inputs -->
    <div class="flex flex-col md:flex-row md:space-x-7 space-y-7 md:space-y-0 mb-7">
      <div class="md:w-1/2">
        <label for="detailed-value1" class="block font-medium text-gray-700">Value</label>
        <div class="mt-2 flex rounded-md">
          <span class="inline-flex items-center rounded-l-md border border-r-0 border-gray-300 bg-gray-50 px-4 text-gray-700 font-medium">
            RM
          </span>
          <input
            id="detailed-value1"
            v-model.number="value1"
            type="number"
            name="value1"
            class="block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-blue-500 focus:ring-blue-500 h-12"
            placeholder="1500"
          />
        </div>
      </div>

      <div class="md:w-1/2">
        <label for="detailed-year1" class="block font-medium text-gray-700">In</label>
        <div v-if="granularity === 'y'" class="mt-2 flex rounded-md">
          <span class="inline-flex items-center rounded-l-md border border-r-0 border-gray-300 bg-gray-50 px-4 text-gray-700 font-medium">
            Year
          </span>
          <input
            id="detailed-year1"
            v-model.lazy.number="year1"
            type="number"
            name="year1"
            :min="activeMinYear"
            :max="meta.maxYear"
            class="block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-blue-500 focus:ring-blue-500 h-12"
            placeholder="2015"
          />
        </div>
        <div v-else class="mt-2 flex rounded-md">
          <select
            v-model.number="month1"
            aria-label="Start month"
            class="rounded-l-md border border-r-0 border-gray-300 bg-gray-50 pl-3 pr-8 text-gray-700 font-medium focus:border-blue-500 focus:outline-none focus:ring-blue-500 h-12"
          >
            <option
              v-for="(mLabel, idx) in MONTH_NAMES"
              :key="mLabel"
              :value="idx + 1"
              :disabled="idx + 1 > maxMonthForYear1"
            >
              {{ mLabel }}
            </option>
          </select>
          <input
            id="detailed-year1"
            v-model.lazy.number="year1"
            type="number"
            name="year1"
            aria-label="Start year"
            :min="activeMinYear"
            :max="meta.maxYear"
            class="block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-blue-500 focus:ring-blue-500 h-12"
            placeholder="2015"
          />
        </div>
      </div>
    </div>

    <!-- Out-of-Range Recovery Notice -->
    <div
      v-if="outOfRangeInfo"
      class="bg-amber-50 border border-amber-200 rounded-md p-3 mb-5 text-sm text-amber-800 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2"
    >
      <span>{{ outOfRangeInfo.message }}</span>
      <button
        type="button"
        @click="outOfRangeInfo.action()"
        class="shrink-0 self-start sm:self-auto px-3 py-1 rounded bg-amber-100 hover:bg-amber-200 text-amber-900 font-medium text-xs border border-amber-300 transition-colors"
      >
        {{ outOfRangeInfo.buttonLabel }}
      </button>
    </div>

    <!-- Result Card -->
    <div class="border p-4 text-center rounded-t-md space-y-4">
      <p class="text-blue-500 text-sm font-bold uppercase tracking-wider">is equivalent to</p>
      <div class="flex justify-center items-baseline space-x-1">
        <p v-if="!isLoadingMonthly && !hasMonthlyError">RM</p>
        <h2
          class="font-medium"
          :class="isLoadingMonthly || hasMonthlyError ? 'text-2xl text-gray-500' : 'text-5xl'"
        >
          {{ displayValue2 }}
        </h2>
      </div>
      <div v-if="hasMonthlyError">
        <button
          type="button"
          @click="retryMonthlyLoad"
          class="text-sm text-blue-600 hover:underline font-medium"
        >
          Retry loading monthly data
        </button>
      </div>

      <div class="flex flex-wrap gap-2 justify-center items-center">
        <p class="text-blue-500 text-sm font-bold uppercase tracking-wider">in</p>
        <select
          v-if="granularity === 'm'"
          v-model.number="month2"
          aria-label="Target month"
          class="border border-gray-300 rounded-md py-1 pl-2.5 pr-7 text-sm font-medium text-gray-700 bg-white focus:border-blue-500 focus:outline-none focus:ring-blue-500"
        >
          <option
            v-for="(mLabel, idx) in MONTH_NAMES"
            :key="mLabel"
            :value="idx + 1"
            :disabled="idx + 1 > maxMonthForYear2"
          >
            {{ mLabel }}
          </option>
        </select>
        <input
          v-model.lazy.number="year2"
          type="number"
          aria-label="Target year"
          :min="activeMinYear"
          :max="meta.maxYear"
          class="border-none p-0 w-20 text-center focus:ring-0"
        />
        <span
          v-if="granularity === 'y' && year2 === meta.ytdYear && meta.ytdMonths < 12"
          class="text-xs text-gray-500"
        >
          (Jan–{{ MONTH_NAMES[meta.ytdMonths - 1] }} YTD)
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import McoicopPicker from './McoicopPicker.vue'
import { detailedCalculatorState } from '@/state/detailedCalculatorState'
import {
  MONTH_NAMES,
  formatYearMonth,
  formatYearMonthLabel,
  getAnnualCPI,
  getAnnualMeta,
  getMaxMonthForYear,
  getMonthlyCPI,
  getNodeByCode,
  loadMonthlyDataset,
  monthlyLoadError,
  monthlyLoaded,
  monthlyLoading,
  parseYearMonth,
} from '@/services/detailedInflationService'
import { trackEvent } from '@/helpers/matomo'
import type { DetailedGranularity } from '@/types/detailedCpi'

const { granularity, selectedCode, year1, month1, year2, month2, value1 } =
  detailedCalculatorState

const meta = getAnnualMeta()

const activeNode = computed(() => getNodeByCode(selectedCode.value))
const activeMinYear = computed(() => activeNode.value?.minYear ?? meta.minYear)

const maxMonthForYear1 = computed(() => getMaxMonthForYear(year1.value))
const maxMonthForYear2 = computed(() => getMaxMonthForYear(year2.value))

watch(year1, (newYear) => {
  if (!Number.isInteger(newYear)) return
  const maxM = getMaxMonthForYear(newYear)
  if (month1.value > maxM) {
    month1.value = maxM
  }
})

watch(year2, (newYear) => {
  if (!Number.isInteger(newYear)) return
  const maxM = getMaxMonthForYear(newYear)
  if (month2.value > maxM) {
    month2.value = maxM
  }
})

const setGranularity = (mode: DetailedGranularity) => {
  if (granularity.value === mode) return
  granularity.value = mode
  if (mode === 'm') {
    month1.value = Math.max(1, Math.min(month1.value, getMaxMonthForYear(year1.value)))
    month2.value = Math.max(1, Math.min(month2.value, getMaxMonthForYear(year2.value)))
    loadMonthlyDataset().catch(() => {
      // Handled via monthlyLoadError
    })
  }
  trackEvent('DetailedCalculator', 'Switch Granularity', mode === 'm' ? 'Monthly' : 'Yearly')
}

const retryMonthlyLoad = () => {
  loadMonthlyDataset().catch(() => {
    // Handled via monthlyLoadError
  })
}

const isLoadingMonthly = computed(
  () => granularity.value === 'm' && monthlyLoading.value && !monthlyLoaded.value
)
const hasMonthlyError = computed(
  () => granularity.value === 'm' && monthlyLoadError.value && !monthlyLoaded.value
)

const cpiLookup = computed(() => {
  if (granularity.value === 'm') {
    if (!Number.isInteger(year1.value) || !Number.isInteger(year2.value)) return {}
    const ym1 = formatYearMonth(year1.value, month1.value)
    const ym2 = formatYearMonth(year2.value, month2.value)
    return getMonthlyCPI(ym1, ym2, selectedCode.value)
  }
  if (!Number.isInteger(year1.value) || !Number.isInteger(year2.value)) return {}
  return getAnnualCPI(year1.value, year2.value, selectedCode.value)
})

const displayValue2 = computed(() => {
  if (isLoadingMonthly.value) return 'Loading...'
  if (hasMonthlyError.value) return 'Failed to load monthly data'
  if (cpiLookup.value.rate === undefined) return 'No Data'

  const base = Number.isFinite(value1.value) ? value1.value : 0
  return (base * cpiLookup.value.rate).toFixed(2)
})

const outOfRangeInfo = computed(() => {
  const node = activeNode.value
  if (!node) return null
  if (isLoadingMonthly.value || hasMonthlyError.value) return null
  if (cpiLookup.value.rate !== undefined) return null

  if (granularity.value === 'y') {
    const p1Invalid = !Number.isInteger(year1.value) || year1.value < node.minYear || year1.value > node.maxYear
    const p2Invalid = !Number.isInteger(year2.value) || year2.value < node.minYear || year2.value > node.maxYear
    const rangeStr = `${node.minYear} – ${node.maxYear}`

    if (p1Invalid && !p2Invalid) {
      const targetYear = !Number.isInteger(year1.value) || year1.value < node.minYear ? node.minYear : node.maxYear
      return {
        message: `Data for ${node.descEn} (${node.code}) is available for ${rangeStr}.`,
        buttonLabel: `Set start to ${targetYear}`,
        action: () => {
          year1.value = targetYear
        },
      }
    }

    return {
      message: `Data for ${node.descEn} (${node.code}) is available for ${rangeStr}.`,
      buttonLabel: 'Clamp to available range',
      action: () => {
        if (!Number.isInteger(year1.value) || year1.value < node.minYear) year1.value = node.minYear
        else if (year1.value > node.maxYear) year1.value = node.maxYear
        if (!Number.isInteger(year2.value) || year2.value < node.minYear) year2.value = node.minYear
        else if (year2.value > node.maxYear) year2.value = node.maxYear
      },
    }
  }

  // Monthly out-of-range
  const minParsed = parseYearMonth(node.minMonth)
  const maxParsed = parseYearMonth(node.maxMonth)
  const ym1 = Number.isInteger(year1.value) ? formatYearMonth(year1.value, month1.value) : ''
  const ym2 = Number.isInteger(year2.value) ? formatYearMonth(year2.value, month2.value) : ''
  const p1Invalid = !ym1 || ym1 < node.minMonth || ym1 > node.maxMonth
  const p2Invalid = !ym2 || ym2 < node.minMonth || ym2 > node.maxMonth
  const rangeStr = `${formatYearMonthLabel(node.minMonth)} – ${formatYearMonthLabel(node.maxMonth)}`

  if (p1Invalid && !p2Invalid) {
    const useMin = !ym1 || ym1 < node.minMonth
    const target = useMin ? minParsed : maxParsed
    const targetLabel = formatYearMonthLabel(useMin ? node.minMonth : node.maxMonth)
    return {
      message: `Data for ${node.descEn} (${node.code}) is available from ${rangeStr}.`,
      buttonLabel: `Set start to ${targetLabel}`,
      action: () => {
        year1.value = target.year
        month1.value = target.month
      },
    }
  }

  return {
    message: `Data for ${node.descEn} (${node.code}) is available from ${rangeStr}.`,
    buttonLabel: 'Clamp to available range',
    action: () => {
      if (!ym1 || ym1 < node.minMonth) {
        year1.value = minParsed.year
        month1.value = minParsed.month
      } else if (ym1 > node.maxMonth) {
        year1.value = maxParsed.year
        month1.value = maxParsed.month
      }
      if (!ym2 || ym2 < node.minMonth) {
        year2.value = minParsed.year
        month2.value = minParsed.month
      } else if (ym2 > node.maxMonth) {
        year2.value = maxParsed.year
        month2.value = maxParsed.month
      }
    },
  }
})
</script>
