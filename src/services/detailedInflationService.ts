import { ref } from 'vue'
import mcoicopTreeJson from '@/assets/data/detailed/mcoicopTree.json'
import cpiDetailedAnnualJson from '@/assets/data/detailed/cpiDetailedAnnual.json'
import type { ChartPoint } from '@/types/chart'
import type {
  DetailedAnnualMeta,
  DetailedCpiAnnualDataset,
  DetailedCpiLookupResult,
  DetailedCpiMonthlyDataset,
  McoicopBreadcrumb,
  McoicopDivision,
  McoicopLevel,
  McoicopNode,
  McoicopTreeData,
} from '@/types/detailedCpi'

const treeData = mcoicopTreeJson as unknown as McoicopTreeData
const annualDataset = cpiDetailedAnnualJson as unknown as DetailedCpiAnnualDataset

export const MONTH_NAMES = [
  'Jan',
  'Feb',
  'Mar',
  'Apr',
  'May',
  'Jun',
  'Jul',
  'Aug',
  'Sep',
  'Oct',
  'Nov',
  'Dec',
] as const

export const LEVEL_LABELS: Record<McoicopLevel, string> = {
  3: 'Group · 3D',
  4: 'Class · 4D',
  5: 'Subclass · 5D',
}

export const LEVEL_LONG_LABELS: Record<McoicopLevel, string> = {
  3: 'Group (3-Digit)',
  4: 'Class (4-Digit)',
  5: 'Subclass (5-Digit)',
}

// Pre-indexed lookup maps built once from mcoicopTree.json
const divisionsList: McoicopDivision[] = treeData.divisions
const divisionMap = new Map<string, McoicopDivision>()
const nodeMap = new Map<string, McoicopNode>()
const groupsByDivision = new Map<string, McoicopNode[]>()
const classesByGroup = new Map<string, McoicopNode[]>()
const subclassesByClass = new Map<string, McoicopNode[]>()

for (const div of divisionsList) {
  divisionMap.set(div.code, div)
  groupsByDivision.set(div.code, [])
}

for (const node of treeData.nodes) {
  nodeMap.set(node.code, node)
  if (node.digits === 3) {
    const list = groupsByDivision.get(node.division)
    if (list) list.push(node)
    if (!classesByGroup.has(node.code)) classesByGroup.set(node.code, [])
  } else if (node.digits === 4) {
    const list = classesByGroup.get(node.group) ?? []
    list.push(node)
    classesByGroup.set(node.group, list)
    if (!subclassesByClass.has(node.code)) subclassesByClass.set(node.code, [])
  } else if (node.digits === 5 && node.classCode) {
    const list = subclassesByClass.get(node.classCode) ?? []
    list.push(node)
    subclassesByClass.set(node.classCode, list)
  }
}

export const LEVEL_COUNTS = {
  all: treeData.nodes.length,
  3: treeData.nodes.filter((n) => n.digits === 3).length,
  4: treeData.nodes.filter((n) => n.digits === 4).length,
  5: treeData.nodes.filter((n) => n.digits === 5).length,
}

// Lazy-loaded monthly dataset state
let monthlyDataset: DetailedCpiMonthlyDataset | null = null
let monthlyDateIndexMap: Map<string, number> | null = null
let monthlyPromise: Promise<DetailedCpiMonthlyDataset> | null = null

export const monthlyLoaded = ref(false)
export const monthlyLoading = ref(false)
export const monthlyLoadError = ref(false)

export const loadMonthlyDataset = (): Promise<DetailedCpiMonthlyDataset> => {
  if (monthlyDataset) {
    return Promise.resolve(monthlyDataset)
  }
  if (monthlyPromise) {
    return monthlyPromise
  }

  monthlyLoading.value = true
  monthlyLoadError.value = false

  monthlyPromise = import('@/assets/data/detailed/cpiDetailedMonthly.json')
    .then((mod) => {
      const data = (mod.default ?? mod) as unknown as DetailedCpiMonthlyDataset
      monthlyDataset = data
      const idxMap = new Map<string, number>()
      data.meta.dates.forEach((ym, idx) => idxMap.set(ym, idx))
      monthlyDateIndexMap = idxMap
      monthlyLoaded.value = true
      monthlyLoading.value = false
      return data
    })
    .catch((err) => {
      monthlyLoading.value = false
      monthlyLoadError.value = true
      monthlyPromise = null
      throw err
    })

  return monthlyPromise
}

export const getAnnualMeta = (): DetailedAnnualMeta => annualDataset.meta

export const getDivisions = (): McoicopDivision[] => divisionsList

export const getDivisionByCode = (code: string): McoicopDivision | undefined => divisionMap.get(code)

export const getNodeByCode = (code: string): McoicopNode | undefined => nodeMap.get(code)

export const getGroupsForDivision = (divisionCode: string): McoicopNode[] =>
  groupsByDivision.get(divisionCode) ?? []

export const getClassesForGroup = (groupCode: string): McoicopNode[] =>
  classesByGroup.get(groupCode) ?? []

export const getSubclassesForClass = (classCode: string): McoicopNode[] =>
  subclassesByClass.get(classCode) ?? []

export const getMaxMonthForYear = (year: number): number => {
  const { minYear, maxYear, ytdYear, ytdMonths } = annualDataset.meta
  if (year < minYear) return 12
  if (year > maxYear) return ytdMonths
  return year === ytdYear ? ytdMonths : 12
}

export const formatYearMonth = (year: number, month: number): string => {
  const m = Math.max(1, Math.min(12, Math.trunc(month)))
  return `${year}-${String(m).padStart(2, '0')}`
}

export const parseYearMonth = (ym: string): { year: number; month: number } => {
  const [yStr, mStr] = ym.split('-')
  return {
    year: Number(yStr),
    month: Number(mStr),
  }
}

export const formatMonthLabel = (year: number, month: number): string => {
  const name = MONTH_NAMES[month - 1] ?? String(month)
  return `${name} ${year}`
}

export const formatYearMonthLabel = (ym: string): string => {
  const { year, month } = parseYearMonth(ym)
  return formatMonthLabel(year, month)
}

export const getBreadcrumb = (code: string): McoicopBreadcrumb | null => {
  const node = nodeMap.get(code)
  if (!node) return null

  const division = divisionMap.get(node.division)
  const group = node.digits === 3 ? node : nodeMap.get(node.group)
  if (!division || !group) return null

  const classNode =
    node.digits === 4
      ? node
      : node.digits === 5 && node.classCode
        ? nodeMap.get(node.classCode)
        : undefined

  const subclassNode = node.digits === 5 ? node : undefined

  return {
    division,
    group,
    classNode,
    subclassNode,
  }
}

export const getParentBenchmarkCode = (
  code: string
): { code: string; label: string; isOverall: boolean } => {
  const node = nodeMap.get(code)
  if (node) {
    if (node.digits === 5 && node.classCode) {
      const parentClass = nodeMap.get(node.classCode)
      if (parentClass) {
        return {
          code: parentClass.code,
          label: `${parentClass.descEn} (Class ${parentClass.code})`,
          isOverall: false,
        }
      }
    } else if (node.digits === 4) {
      const parentGroup = nodeMap.get(node.group)
      if (parentGroup) {
        return {
          code: parentGroup.code,
          label: `${parentGroup.descEn} (Group ${parentGroup.code})`,
          isOverall: false,
        }
      }
    }
  }

  return {
    code: 'overall',
    label: 'Overall CPI (Malaysia)',
    isOverall: true,
  }
}

export const searchMcoicop = (
  query: string,
  levelFilter: McoicopLevel | 'all' = 'all',
  limit = 40
): McoicopNode[] => {
  const trimmed = query.trim().toLowerCase()
  const pool =
    levelFilter === 'all'
      ? treeData.nodes
      : treeData.nodes.filter((n) => n.digits === levelFilter)

  if (!trimmed) {
    return levelFilter === 'all' ? [] : pool.slice(0, limit)
  }

  const tokens = trimmed.split(/\s+/).filter(Boolean)
  const scored: Array<{ node: McoicopNode; rank: number }> = []

  for (const node of pool) {
    const codeLower = node.code.toLowerCase()
    const enLower = node.descEn.toLowerCase()
    const bmLower = node.descBm.toLowerCase()

    const matchesAll = tokens.every(
      (tok) => codeLower.includes(tok) || enLower.includes(tok) || bmLower.includes(tok)
    )
    if (!matchesAll) continue

    let rank = 5
    if (codeLower === trimmed) {
      rank = 0
    } else if (codeLower.startsWith(trimmed)) {
      rank = 1
    } else if (enLower.startsWith(trimmed) || bmLower.startsWith(trimmed)) {
      rank = 2
    } else if (enLower.includes(trimmed)) {
      rank = 3
    } else if (bmLower.includes(trimmed)) {
      rank = 4
    }

    scored.push({ node, rank })
  }

  scored.sort((a, b) => {
    if (a.rank !== b.rank) return a.rank - b.rank
    if (a.node.digits !== b.node.digits) return a.node.digits - b.node.digits
    return a.node.code.localeCompare(b.node.code)
  })

  return scored.slice(0, limit).map((item) => item.node)
}

export const getAnnualCPI = (
  year1: number,
  year2: number,
  code: string
): DetailedCpiLookupResult => {
  const series = code === 'overall' ? annualDataset.overall : annualDataset.series[code]
  if (!series) return {}

  const cpi1 = series[String(year1)]
  const cpi2 = series[String(year2)]
  if (cpi1 === undefined || cpi2 === undefined || cpi1 === 0) {
    return { cpi1, cpi2 }
  }

  return {
    cpi1,
    cpi2,
    rate: cpi2 / cpi1,
  }
}

export const getMonthlyCPI = (
  ym1: string,
  ym2: string,
  code: string
): DetailedCpiLookupResult => {
  // Touch reactive monthlyLoaded flag so Vue computed properties re-evaluate on async load
  if (!monthlyLoaded.value || !monthlyDataset || !monthlyDateIndexMap) {
    return {}
  }

  const tuple = code === 'overall' ? monthlyDataset.overall : monthlyDataset.series[code]
  if (!tuple) return {}

  const idx1 = monthlyDateIndexMap.get(ym1)
  const idx2 = monthlyDateIndexMap.get(ym2)
  const [startIdx, values] = tuple

  const cpi1 =
    idx1 !== undefined && idx1 >= startIdx && idx1 - startIdx < values.length
      ? values[idx1 - startIdx]
      : undefined
  const cpi2 =
    idx2 !== undefined && idx2 >= startIdx && idx2 - startIdx < values.length
      ? values[idx2 - startIdx]
      : undefined

  if (cpi1 === undefined || cpi2 === undefined || cpi1 === 0) {
    return { cpi1, cpi2 }
  }

  return {
    cpi1,
    cpi2,
    rate: cpi2 / cpi1,
  }
}

export const calculateCAGR = (
  cpi1: number,
  cpi2: number,
  spanYears: number
): number | null => {
  const absYears = Math.abs(spanYears)
  if (absYears < 1 || cpi1 <= 0 || cpi2 <= 0) {
    return null
  }
  return (Math.pow(cpi2 / cpi1, 1 / absYears) - 1) * 100
}

export const getDetailedAnnualSeries = (
  year1: number,
  year2: number,
  value1: number,
  code: string
): ChartPoint[] => {
  if (!Number.isInteger(year1) || !Number.isInteger(year2)) return []

  const endpoints = getAnnualCPI(year1, year2, code)
  if (
    endpoints.cpi1 === undefined ||
    endpoints.cpi2 === undefined ||
    endpoints.cpi1 === 0
  ) {
    return []
  }

  const series =
    code === 'overall' ? annualDataset.overall : annualDataset.series[code]
  if (!series) return []

  const baseVal = Number.isFinite(value1) ? value1 : 0
  const startYear = Math.min(year1, year2)
  const endYear = Math.max(year1, year2)
  const points: ChartPoint[] = []

  for (let y = startYear; y <= endYear; y++) {
    const cpiVal = series[String(y)]
    if (cpiVal === undefined) continue
    points.push({
      key: y,
      year: y,
      label: String(y),
      tickLabel: String(y),
      value: baseVal * (cpiVal / endpoints.cpi1),
      metric: cpiVal,
    })
  }

  return points
}

export const getDetailedMonthlySeries = (
  ym1: string,
  ym2: string,
  value1: number,
  code: string
): ChartPoint[] => {
  if (!monthlyLoaded.value || !monthlyDataset || !monthlyDateIndexMap) {
    return []
  }

  const endpoints = getMonthlyCPI(ym1, ym2, code)
  if (
    endpoints.cpi1 === undefined ||
    endpoints.cpi2 === undefined ||
    endpoints.cpi1 === 0
  ) {
    return []
  }

  const tuple =
    code === 'overall' ? monthlyDataset.overall : monthlyDataset.series[code]
  if (!tuple) return []

  const idx1 = monthlyDateIndexMap.get(ym1)
  const idx2 = monthlyDateIndexMap.get(ym2)
  if (idx1 === undefined || idx2 === undefined) return []

  const [startIdx, values] = tuple
  const baseVal = Number.isFinite(value1) ? value1 : 0
  const fromIdx = Math.min(idx1, idx2)
  const toIdx = Math.max(idx1, idx2)
  const points: ChartPoint[] = []

  for (let i = fromIdx; i <= toIdx; i++) {
    const offset = i - startIdx
    if (offset < 0 || offset >= values.length) continue
    const val = values[offset]
    const ym = monthlyDataset.meta.dates[i]
    const { year, month } = parseYearMonth(ym)
    points.push({
      key: ym,
      label: formatMonthLabel(year, month),
      tickLabel: `${MONTH_NAMES[month - 1]} '${String(year).slice(-2)}`,
      value: baseVal * (val / endpoints.cpi1),
      metric: val,
    })
  }

  return points
}
