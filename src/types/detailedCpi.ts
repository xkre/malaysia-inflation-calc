export type McoicopLevel = 3 | 4 | 5

export type DetailedGranularity = 'y' | 'm'

export interface McoicopDivision {
  code: string
  descEn: string
  descBm: string
}

export interface McoicopNode {
  code: string
  digits: McoicopLevel
  division: string
  group: string
  classCode: string | null
  descEn: string
  descBm: string
  minYear: number
  maxYear: number
  minMonth: string
  maxMonth: string
  hasDistinctChildren: boolean
}

export interface McoicopTreeData {
  divisions: McoicopDivision[]
  nodes: McoicopNode[]
}

export interface DetailedAnnualMeta {
  minYear: number
  maxYear: number
  latestMonth: string
  ytdYear: number
  ytdMonths: number
}

export interface DetailedCpiAnnualDataset {
  meta: DetailedAnnualMeta
  overall: Record<string, number>
  series: Record<string, Record<string, number>>
}

export interface DetailedMonthlyMeta {
  minMonth: string
  maxMonth: string
  dates: string[]
}

export interface DetailedCpiMonthlyDataset {
  meta: DetailedMonthlyMeta
  overall: [number, number[]]
  series: Record<string, [number, number[]]>
}

export interface DetailedCpiLookupResult {
  cpi1?: number
  cpi2?: number
  rate?: number
}

export interface McoicopBreadcrumb {
  division: McoicopDivision
  group: McoicopNode
  classNode?: McoicopNode
  subclassNode?: McoicopNode
}
