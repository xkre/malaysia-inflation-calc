import { ref } from 'vue'
import { InflationType } from '../types/InflatitonTypeEnum'
import { MalaysiaPart } from '../types/malaysiaPartEnum'

const url_string = window.location.href
const url = new URL(url_string)

const year1 = Number(url.searchParams.get('y1') ?? 2005)
const year2 = Number(url.searchParams.get('y2') ?? 2020)
const value1 = Number(url.searchParams.get('v1') ?? 1500)
const inflationType = (url.searchParams.get('i') ?? InflationType.General) as InflationType
const part = Number(url.searchParams.get('p') ?? MalaysiaPart.Malaysia) as MalaysiaPart

export const calculatorState = {
  year1: ref(year1),
  year2: ref(year2),
  value1: ref(value1),
  inflationType: ref(inflationType),
  part: ref(part)
}
