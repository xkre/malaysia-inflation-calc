import { ref, watch } from 'vue'
import type { LocationQuery, RouteLocationRaw } from 'vue-router'
import { router } from '@/router'
import { showInfo } from '@/state/infoState'
import {
  getAnnualMeta,
  getMaxMonthForYear,
  getNodeByCode,
  loadMonthlyDataset,
} from '@/services/detailedInflationService'
import type { DetailedGranularity } from '@/types/detailedCpi'

const DEFAULT_CODE = '011'
const meta = getAnnualMeta()

const granularity = ref<DetailedGranularity>('y')
const selectedCode = ref<string>(DEFAULT_CODE)
const year1 = ref<number>(2015)
const month1 = ref<number>(1)
const year2 = ref<number>(Math.min(2025, meta.maxYear))
const month2 = ref<number>(getMaxMonthForYear(Math.min(2025, meta.maxYear)))
const value1 = ref<number>(1500)

const readQueryString = (val: unknown): string | null => {
  if (typeof val === 'string') return val
  if (Array.isArray(val) && typeof val[0] === 'string') return val[0]
  return null
}

const parsePositiveInt = (raw: string | null): number | null => {
  if (raw === null || raw.trim() === '') return null
  const num = Number(raw)
  return Number.isInteger(num) ? num : null
}

const clampMonth = (month: number, year: number): number => {
  const maxM = getMaxMonthForYear(year)
  return Math.max(1, Math.min(maxM, month))
}

export const hydrateDetailedStateFromQuery = (query: LocationQuery | Record<string, unknown>) => {
  const gRaw = readQueryString(query.g)
  if (gRaw === 'm' || gRaw === 'y') {
    granularity.value = gRaw
  }

  const cRaw = readQueryString(query.c)
  if (cRaw && getNodeByCode(cRaw)) {
    selectedCode.value = cRaw
  }

  const y1Raw = parsePositiveInt(readQueryString(query.y1))
  if (y1Raw !== null) {
    year1.value = y1Raw
  }

  const y2Raw = parsePositiveInt(readQueryString(query.y2))
  if (y2Raw !== null) {
    year2.value = y2Raw
  }

  const m1Raw = parsePositiveInt(readQueryString(query.m1))
  if (m1Raw !== null) {
    month1.value = clampMonth(m1Raw, year1.value)
  } else {
    month1.value = clampMonth(month1.value, year1.value)
  }

  const m2Raw = parsePositiveInt(readQueryString(query.m2))
  if (m2Raw !== null) {
    month2.value = clampMonth(m2Raw, year2.value)
  } else {
    month2.value = clampMonth(month2.value, year2.value)
  }

  const v1Raw = readQueryString(query.v1)
  if (v1Raw !== null && v1Raw.trim() !== '') {
    const parsedVal = Number(v1Raw)
    if (Number.isFinite(parsedVal)) {
      value1.value = parsedVal
    }
  }

  if (granularity.value === 'm') {
    loadMonthlyDataset().catch(() => {
      // Handled reactively via monthlyLoadError in UI
    })
  }
}

export const setupDetailedRouteWatch = (): (() => void) => {
  return watch(
    [granularity, selectedCode, year1, month1, year2, month2, value1, showInfo],
    () => {
      if (router.currentRoute.value.name !== 'detailed') return

      const query: Record<string, string | number> = {
        g: granularity.value,
        y1: year1.value,
        y2: year2.value,
        v1: value1.value,
        c: selectedCode.value,
        s: showInfo.value ? 1 : 0,
      }

      if (granularity.value === 'm') {
        query.m1 = month1.value
        query.m2 = month2.value
      }

      const location: RouteLocationRaw = {
        name: 'detailed',
        query,
      }

      router.replace(location)
    }
  )
}

export const detailedCalculatorState = {
  granularity,
  selectedCode,
  year1,
  month1,
  year2,
  month2,
  value1,
}
