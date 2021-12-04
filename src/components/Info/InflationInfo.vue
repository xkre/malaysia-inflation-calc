<template>
  <div class="flex flex-col items-center justify-center container flex-wrap">
    <div v-for="yearInflation in yearlyInflation" :key="yearInflation.year" class="flex flex-row yearly justify-items-start justify-start content-center items-start text-left">
      <div class="year"> {{ yearInflation.year }}: </div>    
      <div class="inflation"> {{ yearInflation.inflation.toFixed(2) }} </div>    
      <div class="pl-2"> {{ yearInflation.price.toFixed(2) }} </div>    
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from '@vue/reactivity'
import { getYearlyInflation } from '../../services/inflationService'
import { calculatorState } from '../../state/calculatorState'

const yearlyInflation = computed(() => {
  const { year1, year2, value1 } = calculatorState

  const inflationYear = getYearlyInflation(year1.value, year2.value)
  const inflationYearPrice = []

  let yearPrice = value1.value

  for(const year of inflationYear) {
    yearPrice = yearPrice * year.inflation / 100 + yearPrice
    const inflationprice = {
      year: year.year,
      inflation: year.inflation,
      price: yearPrice
    }

    inflationYearPrice.push(inflationprice)
  }

  return inflationYearPrice
})
</script>

<style lang="scss" scoped>
.year{
  @apply flex pr-1  text-left;
}



.container {
  max-height: calc(100vh - 20rem);
}
</style>