<template>
  <div>
    <select v-model="inflationType" class="mb-8">
      <option :value="InflationType.General"> General Inflation </option>
      <option :value="InflationType.TotalCPI"> Overall CPI </option>
      <option :value="InflationType.Food"> Food Prices </option>
      <option :value="InflationType.AlcoholTobacco"> Alcoholic Beverages and Tobacco </option>
      <option :value="InflationType.Clothing"> Clothing and Footwear </option>
      <option :value="InflationType.Housing"> Housing, Water, Electricity, Gas and Other Fuels </option>
      <option :value="InflationType.Furnishing"> Furnishings, Households Equipment and Routine Household Maintenance </option>
      <option :value="InflationType.Health"> Health </option>
      <option :value="InflationType.Transport"> Transport </option>
      <option :value="InflationType.Communication"> Communication </option>
      <option :value="InflationType.Recreative"> Recreation Services and Culture </option>
      <option :value="InflationType.Education"> Education </option>
      <option :value="InflationType.RestaurantHotels"> Restaurants and Hotels </option>
      <option :value="InflationType.Misc"> Miscellaneous Goods and Services </option>
    </select>
    <p>
      RM <input v-model.number="value1" class="value-input">
      in <input type="number" v-model.lazy.number="year1" class="year-input">
      is equivalent to RM <input v-model="value2" disabled class="value-input">
      in <input type="number" v-model.lazy.number="year2" class="year-input">
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue"
import { getCumulativeInflation, getCPI } from '../services/inflationService'
import { calculatorState } from "../state/calculatorState"
import { InflationType } from '../types/InflatitonTypeEnum'

const { year1, year2, value1, inflationType } = calculatorState

const value2 = computed(() => {
  try {
    let inflationRate: number

    if (inflationType.value === InflationType.General) {
      inflationRate = getCumulativeInflation(year1.value, year2.value)
    } else {
      inflationRate = getCPI(year1.value, year2.value, inflationType.value)
    }

    if (year1.value < year2.value) {

    }

    return (value1.value * inflationRate).toFixed(2)
  } catch (er) {
    return er
  }
})
</script>

<style lang="scss" scoped>
input {
  @apply border-b-2 border-blue-500;
  @apply px-2 mx-2;

  &.value-input {
    @apply w-32;
  }

  &.year-input {
    @apply w-16;
    @apply pr-0;
  }

  &:disabled {
    @apply rounded-t-md cursor-not-allowed;
  }
}

select {
  @apply border-blue-500 border-b-2;
}
</style>