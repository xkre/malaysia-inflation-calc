import { ref } from 'vue'
import { getQueryParam } from '@/services/routeService'
import { InflationType } from '@/types/InflatitonTypeEnum'
import { MalaysiaPart } from '@/types/malaysiaPartEnum'

const year1 = Number(getQueryParam('y1') ?? 2005)
const year2 = Number(getQueryParam('y2') ?? 2022)
const value1 = Number(getQueryParam('v1') ?? 1500)
const inflationType = (getQueryParam('i') ?? InflationType.TotalCPI) as InflationType
const part = Number(getQueryParam('p') ?? MalaysiaPart.Malaysia) as MalaysiaPart

export const calculatorState = {
  year1: ref(year1),
  year2: ref(year2),
  value1: ref(value1),
  inflationType: ref(inflationType),
  part: ref(part)
}
