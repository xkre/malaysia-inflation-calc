<template>
  <div>
    <ul v-for="yearInflation in yearlyInflation" :key="yearInflation.year">
      <li class="flex space-x-2 py-1">
        <div class="font-semibold"> {{ yearInflation.year }}: </div>    
        <div class="pl-2"> {{ yearInflation.inflation.toFixed(2) }} </div>    
        <div class="pl-2"> {{ yearInflation.value.toFixed(2) }} </div>    
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
type YearlyInflationValue = YearlyInflation & {
  value: number;
}
</script>

<script setup lang="ts">
import { computed } from '@vue/reactivity'
import { getYearlyInflation } from '@/services/inflationService'
import { calculatorState } from '@/state/calculatorState'

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
