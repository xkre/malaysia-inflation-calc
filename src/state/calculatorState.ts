import { reactive, ref } from 'vue'
import { InflationType } from '../types/InflatitonTypeEnum'

export const calculatorState = {
  year1: ref(2005),
  year2: ref(2020),
  value1: ref(1500),
  inflationType: ref(InflationType.General)
}