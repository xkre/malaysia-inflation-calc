<template>
  <div>
    <div class="mb-7">
      <label for="type" class="block font-medium text-gray-700">Type</label>
      <select id="type" v-model="inflationType" @change="typeChanged" class="mt-2 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500">
        <option :value="InflationType.General"> General Inflation (1960 - 2025) </option>
        <option :value="InflationType.TotalCPI"> Overall CPI (1960 - 2026) </option>
        <option :value="InflationType.Food"> Food (1980 - 2026) </option>
        <option :value="InflationType.AlcoholTobacco"> Alcoholic Beverages and Tobacco (1980 - 2026) </option>
        <option :value="InflationType.Clothing"> Clothing and Footwear (1980 - 2026) </option>
        <option :value="InflationType.Housing"> Housing, Water, Electricity, Gas and Other Fuels (1980 - 2026) </option>
        <option :value="InflationType.Furnishing"> Furnishings, Households Equipment and Routine Household Maintenance (1980 - 2026) </option>
        <option :value="InflationType.Health"> Health (1980 - 2026) </option>
        <option :value="InflationType.Transport"> Transport (1980 - 2026) </option>
        <option :value="InflationType.Communication"> Communication (2003 - 2026) </option>
        <option :value="InflationType.Recreative"> Recreation Services and Culture (1980 - 2026) </option>
        <option :value="InflationType.Education"> Education (2003 - 2026) </option>
        <option :value="InflationType.RestaurantHotels"> Restaurants and Hotels (2003 - 2026) </option>
        <option :value="InflationType.Insurance"> Insurance & Financial Services (2010 - 2026) </option>
        <option :value="InflationType.Misc"> Miscellaneous Goods and Services (2003 - 2026) </option>
        <option :value="InflationType.BigMac"> Big Mac Index (2000 - 2026) </option>
      </select>
    </div>
    <div class="mb-7" v-if="inflationType !== InflationType.General && inflationType !== InflationType.BigMac">
      <label for="part" class="block font-medium text-gray-700">State / Region</label>
      <select id="part" v-model.number="part" class="mt-2 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500">
        <optgroup label="National & Macro Regions">
          <option v-for="opt in macroRegionOptions" :key="opt.label" :value="opt.value">
            {{ formatPartOptionLabel(opt.label, opt.value) }}
          </option>
        </optgroup>
        <optgroup label="States & Federal Territories">
          <option v-for="opt in stateOptions" :key="opt.label" :value="opt.value">
            {{ formatPartOptionLabel(opt.label, opt.value) }}
          </option>
        </optgroup>
      </select>
      <p v-if="isDifferentFromMain && selectedPartYearRange" class="mt-2 text-sm text-gray-500">
        Data available for selected state/region: {{ selectedPartYearRange.min }} - {{ selectedPartYearRange.max }}
      </p>
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
import { getCumulativeInflation, getCPIRate, getAvailableYearRange } from '@/services/inflationService'
import { InflationType } from '@/types/InflatitonTypeEnum'
import { MalaysiaPart } from "@/types/malaysiaPartEnum"
import { trackEvent } from "@/helpers/matomo"

const { year1, year2, value1, inflationType, part } = calculatorState

const macroRegionOptions = [
  { value: MalaysiaPart.Malaysia, label: 'Malaysia (National)' },
  { value: MalaysiaPart.Semenanjung, label: 'Semenanjung (Peninsular Malaysia)' },
  { value: MalaysiaPart.SabahLabuan, label: 'Sabah & Labuan' },
  { value: MalaysiaPart.Sarawak, label: 'Sarawak' },
]

const stateOptions = [
  { value: MalaysiaPart.Johor, label: 'Johor' },
  { value: MalaysiaPart.Kedah, label: 'Kedah' },
  { value: MalaysiaPart.Kelantan, label: 'Kelantan' },
  { value: MalaysiaPart.Melaka, label: 'Melaka' },
  { value: MalaysiaPart.NegeriSembilan, label: 'Negeri Sembilan' },
  { value: MalaysiaPart.Pahang, label: 'Pahang' },
  { value: MalaysiaPart.Perak, label: 'Perak' },
  { value: MalaysiaPart.Perlis, label: 'Perlis' },
  { value: MalaysiaPart.PulauPinang, label: 'Pulau Pinang' },
  { value: MalaysiaPart.Sabah, label: 'Sabah (State)' },
  { value: MalaysiaPart.Sarawak, label: 'Sarawak (State)' },
  { value: MalaysiaPart.Selangor, label: 'Selangor' },
  { value: MalaysiaPart.Terengganu, label: 'Terengganu' },
  { value: MalaysiaPart.KualaLumpur, label: 'W.P. Kuala Lumpur' },
  { value: MalaysiaPart.Labuan, label: 'W.P. Labuan' },
  { value: MalaysiaPart.Putrajaya, label: 'W.P. Putrajaya' },
]

const mainYearRange = computed(() => getAvailableYearRange(inflationType.value, MalaysiaPart.Malaysia))
const selectedPartYearRange = computed(() => getAvailableYearRange(inflationType.value, part.value))

const isDifferentFromMain = computed(() => {
  if (!mainYearRange.value || !selectedPartYearRange.value) return false
  return (
    selectedPartYearRange.value.min !== mainYearRange.value.min ||
    selectedPartYearRange.value.max !== mainYearRange.value.max
  )
})

const formatPartOptionLabel = (baseLabel: string, partValue: MalaysiaPart): string => {
  const range = getAvailableYearRange(inflationType.value, partValue)
  const main = mainYearRange.value
  if (range && (!main || range.min !== main.min || range.max !== main.max)) {
    return `${baseLabel} (${range.min} - ${range.max})`
  }
  return baseLabel
}

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
