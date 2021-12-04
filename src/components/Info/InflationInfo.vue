<template>
  <div class="flex flex-col container flex-wrap">
    <div v-for="yearInflation in yearlyInflation" :key="yearInflation.year" class="flex flex-row self-center">
      <div class=""> {{ yearInflation.year }}: </div>    
      <div class="pl-2"> {{ yearInflation.inflation.toFixed(2) }} </div>    
      <div class="pl-2"> {{ yearInflation.value.toFixed(2) }} </div>    
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from '@vue/reactivity'
import { getYearlyInflation } from '../../services/inflationService'
import { calculatorState } from '../../state/calculatorState'

type YearlyInflationValue = YearlyInflation & {
  value: number;
}

const yearlyInflation = computed((): YearlyInflationValue [] => {
  const { year1, year2, value1 } = calculatorState

  const yearlyInflation = getYearlyInflation(year1.value, year2.value)
  const yearlyInflationPrices: YearlyInflationValue [] = []

  let compoundingValue = value1.value

  for (const year of yearlyInflation) {
    compoundingValue = compoundingValue * year.inflation / 100 + compoundingValue

    const inflationprice = {
      year: year.year,
      inflation: year.inflation,
      value: compoundingValue
    }

    yearlyInflationPrices.push(inflationprice)
  }

  return yearlyInflationPrices
})
</script>

<style lang="scss" scoped>
.container {
  max-height: calc(100vh - 20rem);
}
</style>