<template>
  <div>
    <div class="mb-7">
      <label for="type" class="block font-medium text-gray-700">Type</label>
      <select id="type" v-model="inflationType" @change="typeChanged" class="mt-2 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500">
        <option :value="InflationType.General"> General Inflation (1960 - 2023) </option>
        <option :value="InflationType.TotalCPI"> Overall CPI (2000 - 2023)</option>
        <option :value="InflationType.Food"> Food (2000 - 2023) </option>
        <option :value="InflationType.AlcoholTobacco"> Alcoholic Beverages and Tobacco (2000 - 2023) </option>
        <option :value="InflationType.Clothing"> Clothing and Footwear (2000 - 2023) </option>
        <option :value="InflationType.Housing"> Housing, Water, Electricity, Gas and Other Fuels (2000 - 2023) </option>
        <option :value="InflationType.Furnishing"> Furnishings, Households Equipment and Routine Household Maintenance (2000 - 2023) </option>
        <option :value="InflationType.Health"> Health (2000 - 2023)</option>
        <option :value="InflationType.Transport"> Transport (2000 - 2023) </option>
        <option :value="InflationType.Communication"> Communication (2000 - 2023) </option>
        <option :value="InflationType.Recreative"> Recreation Services and Culture (2000 - 2023) </option>
        <option :value="InflationType.Education"> Education (2000 - 2023) </option>
        <option :value="InflationType.RestaurantHotels"> Restaurants and Hotels (2000 - 2023) </option>
        <option :value="InflationType.Misc"> Miscellaneous Goods and Services (2000 - 2023) </option>
        <option :value="InflationType.BigMac"> Big Mac Index (2000 - 2024) </option>
      </select>
    </div>
    <div class="flex flex-col md:flex-row md:space-x-7 space-y-4 md:space-y-0 mb-7" v-if="inflationType !== InflationType.General">
      <div class="flex items-center">
        <input id="MalaysiaPart.Malaysia" v-model="part" :value="MalaysiaPart.Malaysia" name="MalaysiaPart" type="radio" class="h-6 w-6 border-gray-300 text-blue-600 focus:ring-blue-500">
        <label for="MalaysiaPart.Malaysia" class="ml-3 block font-medium text-gray-700">Malaysia</label>
      </div>
      <div class="flex items-center">
        <input id="MalaysiaPart.Semenanjung" v-model="part" :value="MalaysiaPart.Semenanjung" name="MalaysiaPart" type="radio" class="h-6 w-6 border-gray-300 text-blue-600 focus:ring-blue-500">
        <label for="MalaysiaPart.Semenanjung" class="ml-3 block font-medium text-gray-700">Semenanjung</label>
      </div>
      <div class="flex items-center">
        <input id="MalaysiaPart.SabahLabuan" v-model="part" :value="MalaysiaPart.SabahLabuan" name="MalaysiaPart" type="radio" class="h-6 w-6 border-gray-300 text-blue-600 focus:ring-blue-500">
        <label for="MalaysiaPart.SabahLabuan" class="ml-3 block font-medium text-gray-700">Sabah & Labuan</label>
      </div>
      <div class="flex items-center">
        <input id="MalaysiaPart.Sarawak" v-model="part" :value="MalaysiaPart.Sarawak" name="MalaysiaPart" type="radio" class="h-6 w-6 border-gray-300 text-blue-600 focus:ring-blue-500">
        <label for="MalaysiaPart.Sarawak" class="ml-3 block font-medium text-gray-700">Sarawak</label>
      </div>
    </div>
    <div class="flex flex-col md:flex-row md:space-x-7 space-y-7 md:space-y-0 mb-7">
      <div class="md:w-1/2">
        <label for="value1" class="block font-medium text-gray-700">Value</label>
        <div class="mt-2 flex rounded-md">
          <span class="inline-flex items-center rounded-l-md border border-r-0 border-gray-300 bg-gray-50 px-4 text-gray-700 font-medium">RM</span>
          <input type="number" name="value1" v-model.number="value1" id="value1" class="block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-blue-500 focus:ring-blue-500 h-12" placeholder="1500">
        </div>
      </div>
      <div class="md:w-1/2">
        <label for="year1" class="block font-medium text-gray-700">In</label>
        <div class="mt-2 flex rounded-md">
          <span class="inline-flex items-center rounded-l-md border border-r-0 border-gray-300 bg-gray-50 px-4 text-gray-700 font-medium">Year</span>
          <input type="number" name="year1" v-model.lazy.number="year1" id="year1" class="block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-blue-500 focus:ring-blue-500 h-12" placeholder="2020">
        </div>
      </div>
    </div>
    <div class="border p-4 text-center rounded-t-md space-y-4">
      <p class="text-blue-500 text-sm font-bold uppercase tracking-wider">is equivalent to</p>
      <div class="flex justify-center space-x-1">
        <p>RM</p>
        <h2 class="text-5xl font-medium">{{ value2 }}</h2>
      </div>
      <div class="flex space-x-2 justify-center items-center">
        <p class="text-blue-500 text-sm font-bold uppercase tracking-wider">in</p>
        <input type="number" v-model.lazy.number="year2" class="border-none p-0 w-20">
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { calculatorState } from "../state/calculatorState"
</script>

<script setup lang="ts">
import { computed } from "vue"
import { getCumulativeInflation, getCPIRate } from '@/services/inflationService'
import { InflationType } from '@/types/InflatitonTypeEnum'
import { MalaysiaPart } from "@/types/malaysiaPartEnum"
import { trackEvent } from "@/helpers/matomo"

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
      // trackEvent('Exception', er, 'Calculator')

      return er
    }

    console.error(er)
    return 'Error'
  }
})

const typeChanged = () => {
  const val = inflationType.value
  trackEvent('Calculator', 'Change Type', val)
}

</script>
