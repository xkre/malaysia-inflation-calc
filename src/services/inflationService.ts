import { 
  cpiMalaysia, 
  cpiSabahLabuan, 
  cpiSarawak, 
  cpiSemenanjung, 
  cpiStates,
  inflation 
} from "../assets/data"
import { bigMacIndex } from "@/assets/data/misc/bigMacIndex"

import { InflationType } from "@/types/InflatitonTypeEnum"
import { MalaysiaPart } from "@/types/malaysiaPartEnum"

const inflationYears = Object.keys(inflation).map(x => parseInt(x))
const beginYear = inflationYears[0]
const endYear = inflationYears[inflationYears.length-1]

export const getYearlyInflation = (year1: number, year2: number): YearlyInflation[] => {
  const smaller = year1 < year2 ? year1 : year2
  const larger = year1 > year2 ? year1 : year2

  if (smaller < beginYear) throw 'No Data'
  if (larger > endYear) throw 'No Data'

  const yearlyInflation = Object.keys(inflation)
    .map(x => Number(x))
    .filter(x => x > smaller && x <= larger)
    .map(x => ({
      year: x,
      inflation: inflation[x]
    }))

  return yearlyInflation
}

export const getCumulativeInflation = (year1: number, year2: number): number => {
  if (year1 === year2) return 1

  const yearlyInflation = getYearlyInflation(year1, year2)

  if (yearlyInflation.length === 0) {
    throw 'No data'
  }

  console.debug({ inflation })
  console.debug({ yearlyInflation, length: yearlyInflation.length })

  let cumulInflation = 1

  if (year2 > year1) {
    for (const yearInflation of yearlyInflation) {
      const rate = yearInflation.inflation

      cumulInflation = cumulInflation + rate * cumulInflation / 100
    }
  } else {
    yearlyInflation.reverse()

    for (const yearInflation of yearlyInflation) {
      const rate = yearInflation.inflation

      cumulInflation = cumulInflation - rate * cumulInflation / 100
    }
  }

  console.debug(`Cumulative inflation from ${year1} to ${year2}:`, cumulInflation)

  return cumulInflation
}

const getCPIData = (part: MalaysiaPart): CPIDataset => {
  let cpiData: CPIDataset

  if (part === MalaysiaPart.Malaysia) {
    cpiData = cpiMalaysia
  } else if (part === MalaysiaPart.Semenanjung) {
    cpiData = cpiSemenanjung
  } else if (part === MalaysiaPart.SabahLabuan) {
    cpiData = cpiSabahLabuan
  } else if (part === MalaysiaPart.Sarawak) {
    cpiData = cpiSarawak
  } else if (cpiStates[part]) {
    cpiData = cpiStates[part]!
  } else {
    throw 'Error: Malaysia Part selection'
  }

  return cpiData
}

export const getCPI = (year1: number, year2: number, type: InflationType, part: MalaysiaPart): {year1?: number, year2?: number} => {
  if (type === InflationType.BigMac) {
    const year1Cpi = bigMacIndex[year1]
    const year2Cpi = bigMacIndex[year2]

    return {
      year1: year1Cpi,
      year2: year2Cpi
    }
  }
  else {
    const cpiData = getCPIData(part)

    const year1Cpi = cpiData[year1]?.[type]
    const year2Cpi = cpiData[year2]?.[type]
  
    return {
      year1: year1Cpi,
      year2: year2Cpi
    }
  }
}

export const getCPIRate = (year1: number, year2: number, type: InflationType, part: MalaysiaPart): number => {
  if (type === InflationType.General) throw 'Error'

  const cpiData = getCPI(year1, year2, type, part)

  const year1Cpi = cpiData.year1
  const year2Cpi = cpiData.year2

  if (year1Cpi === undefined || year2Cpi === undefined) throw 'No Data'

  const relativePrice = year2Cpi / year1Cpi

  console.debug({ year1Cpi, year2Cpi, relativePrice })

  return relativePrice
}

/**
 * Returns the inclusive min/max year range with available data for a given inflation type and region/state.
 */
export const getAvailableYearRange = (
  type: InflationType,
  part: MalaysiaPart = MalaysiaPart.Malaysia
): { min: number; max: number } | null => {
  if (type === InflationType.General) {
    return { min: beginYear, max: endYear }
  }

  if (type === InflationType.BigMac) {
    const years = Object.keys(bigMacIndex).map(Number).sort((a, b) => a - b)
    return years.length ? { min: years[0], max: years[years.length - 1] } : null
  }

  const cpiData = getCPIData(part)
  const years = Object.keys(cpiData)
    .map(Number)
    .filter(yr => cpiData[yr]?.[type] !== undefined)
    .sort((a, b) => a - b)

  return years.length ? { min: years[0], max: years[years.length - 1] } : null
}

export interface YearlyProgressionPoint {
  year: number
  value: number
  metric?: number
  yoyPct?: number
}

/**
 * Returns chronological year-by-year equivalent RM progression for CPI and Big Mac modes.
 * Never throws; returns an empty array if inputs or endpoints have no data.
 */
export const getCPISeries = (
  year1: number,
  year2: number,
  value1: number,
  type: InflationType,
  part: MalaysiaPart
): YearlyProgressionPoint[] => {
  if (type === InflationType.General) return []
  if (!Number.isInteger(year1) || !Number.isInteger(year2)) return []

  const endpoints = getCPI(year1, year2, type, part)
  if (endpoints.year1 === undefined || endpoints.year2 === undefined || endpoints.year1 === 0) {
    return []
  }

  const baseVal = Number.isFinite(value1) ? value1 : 0
  const startYear = Math.min(year1, year2)
  const endYear = Math.max(year1, year2)
  const points: YearlyProgressionPoint[] = []
  let prevMetric: number | undefined

  for (let y = startYear; y <= endYear; y++) {
    const cpiVal =
      type === InflationType.BigMac ? bigMacIndex[y] : getCPIData(part)[y]?.[type]

    if (cpiVal === undefined) continue

    const yoyPct =
      prevMetric !== undefined && prevMetric !== 0
        ? ((cpiVal - prevMetric) / prevMetric) * 100
        : undefined

    points.push({
      year: y,
      value: baseVal * (cpiVal / endpoints.year1),
      metric: cpiVal,
      yoyPct,
    })

    prevMetric = cpiVal
  }

  return points
}

/**
 * Returns chronological year-by-year compounded RM progression for General Inflation mode.
 * Supports forward (year2 > year1) and backward (year2 < year1) ranges without throwing.
 */
export const getGeneralInflationSeries = (
  year1: number,
  year2: number,
  value1: number
): YearlyProgressionPoint[] => {
  if (!Number.isInteger(year1) || !Number.isInteger(year2)) return []

  const smaller = Math.min(year1, year2)
  const larger = Math.max(year1, year2)
  if (smaller < beginYear || larger > endYear) return []

  const baseVal = Number.isFinite(value1) ? value1 : 0

  if (year1 === year2) {
    const rate = inflation[year1]
    return rate === undefined ? [] : [{ year: year1, value: baseVal, metric: rate }]
  }

  if (year2 > year1) {
    const points: YearlyProgressionPoint[] = [
      { year: year1, value: baseVal, metric: inflation[year1] },
    ]
    let curr = baseVal

    for (let y = year1 + 1; y <= year2; y++) {
      const rate = inflation[y]
      if (rate === undefined) return []
      curr = curr + (rate * curr) / 100
      points.push({
        year: y,
        value: curr,
        metric: rate,
        yoyPct: rate,
      })
    }

    return points
  }

  // Backward range (year2 < year1): step backwards from year1, then reverse chronologically
  const reversedPoints: YearlyProgressionPoint[] = [
    { year: year1, value: baseVal, metric: inflation[year1], yoyPct: inflation[year1] },
  ]
  let curr = baseVal

  for (let y = year1; y >= year2 + 1; y--) {
    const rate = inflation[y]
    if (rate === undefined) return []
    curr = curr - (rate * curr) / 100
    const prevYear = y - 1
    reversedPoints.push({
      year: prevYear,
      value: curr,
      metric: inflation[prevYear],
      yoyPct: inflation[prevYear],
    })
  }

  return reversedPoints.reverse()
}
