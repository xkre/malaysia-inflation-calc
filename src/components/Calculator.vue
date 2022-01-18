<template>
  <div>
    <select v-model="inflationType" class="max-w-full">
      <option :value="InflationType.General"> General Inflation </option>
      <option :value="InflationType.TotalCPI"> Overall CPI </option>
      <option :value="InflationType.Food"> Food </option>
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
    <div class="flex-col md:flex-row md:items-center items-start radio-list mt-8" v-if="inflationType !== InflationType.General">
      <label> <input type="radio" name="part" v-model="part" :value="MalaysiaPart.Malaysia"> Malaysia </label>
      <label> <input type="radio" name="part" v-model="part" :value="MalaysiaPart.Semenanjung"> Semenanjung </label>
      <label> <input type="radio" name="part" v-model="part" :value="MalaysiaPart.SabahLabuan"> Sabah & Labuan </label>
      <label> <input type="radio" name="part" v-model="part" :value="MalaysiaPart.Sarawak"> Sarawak </label>
    </div>
    <p class="mt-8">
      RM <input type="number" v-model.number="value1" class="value-input">
      in <input type="number" v-model.lazy.number="year1" class="year-input">
      is equivalent to RM <input v-model="value2" disabled class="value-input">
      in <input type="number" v-model.lazy.number="year2" class="year-input">
    </p>
  </div>
</template>

<script lang="ts">
import { calculatorState } from "../state/calculatorState"
</script>

<script setup lang="ts">
import { computed } from "vue"
import { getCumulativeInflation, getCPIRate } from '../services/inflationService'
import { InflationType } from '../types/InflatitonTypeEnum'
import { MalaysiaPart } from "../types/malaysiaPartEnum"

const { year1, year2, value1, inflationType, part } = calculatorState

const value2 = computed((): string => {
  try {
    let inflationRate: number

    if (inflationType.value === InflationType.General) {
      inflationRate = getCumulativeInflation(year1.value, year2.value)
    } else {
      inflationRate = getCPIRate(year1.value, year2.value, inflationType.value, part.value)
    }

    return (value1.value * inflationRate).toFixed(2)
  } catch (er) {
    if (typeof er === 'string') {
      return er
    }

    console.error(er)
    return 'Error'
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
  }

  &[type="number"]{
    @apply pr-0;
  }

  &:disabled {
    @apply rounded-t-md cursor-not-allowed;
  }
}

select {
  @apply border-blue-500 border-b-2;
}

.radio-list{
  @apply flex px-4;
  @apply justify-center;

  label {
    @apply relative px-4 mx-4;
    @apply cursor-pointer;
    
    input[type="radio"] {
      @apply absolute -left-3 top-1;
    }
  }
}
</style>
