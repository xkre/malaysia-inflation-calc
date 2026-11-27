import { ref } from 'vue'
import { getQueryParam } from '@/services/routeService'
import { InflationType } from '@/types/InflatitonTypeEnum'
import { MalaysiaPart } from '@/types/malaysiaPartEnum'

const isInitialSimpleRoute = !window.location.pathname.startsWith('/detailed')

const year1 = Number((isInitialSimpleRoute ? getQueryParam('y1') : null) ?? 2005)
const year2 = Number((isInitialSimpleRoute ? getQueryParam('y2') : null) ?? 2025)
const value1 = Number((isInitialSimpleRoute ? getQueryParam('v1') : null) ?? 1500)
const inflationType = ((isInitialSimpleRoute ? getQueryParam('i') : null) ?? InflationType.TotalCPI) as InflationType
const part = Number((isInitialSimpleRoute ? getQueryParam('p') : null) ?? MalaysiaPart.Malaysia) as MalaysiaPart

export const calculatorState = {
  year1: ref(year1),
  year2: ref(year2),
  value1: ref(value1),
  inflationType: ref(inflationType),
  part: ref(part)
}
