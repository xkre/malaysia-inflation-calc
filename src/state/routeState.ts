import { calculatorState } from "./calculatorState"
import { showInfo } from "../state/infoState"
import { watch } from 'vue'
import { router } from "../router"

import type { LocationAsPath, RouteLocationOptions, RouteQueryAndHash } from "vue-router"

const {year1, year2, value1, inflationType, part} = calculatorState

export const setupWatch = () => {
  watch([year1, year2, value1, inflationType, part, showInfo], () => {
    const state = {
      y1: year1.value,
      y2: year2.value,
      v1: value1.value,
      i: inflationType.value,
      p: part.value,
      s: showInfo.value ? 1 : 0
    }

    const location: (RouteQueryAndHash & LocationAsPath & RouteLocationOptions) = {
      path: '/',
      query: state
    }

    router.replace(location)
  })
}
