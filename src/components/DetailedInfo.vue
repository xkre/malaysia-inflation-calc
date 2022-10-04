<template>
  <div class="flex flex-col">
    <button class="text-blue-500 font-semibold bg-blue-50 rounded-b-md py-2.5 w-full space-x-2 flex justify-center" @click="togleInfo"> 
      <span>{{ showInfo ? 'Hide' : 'More'}} Info </span>
      <!-- icon plus -->
      <svg v-if="!showInfo" xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-plus" width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <line x1="5" y1="12" x2="19" y2="12"></line>
      </svg>
      <!-- icon minus -->
      <svg v-else xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-minus" width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
        <line x1="5" y1="12" x2="19" y2="12"></line>
      </svg>
    </button>
    <template v-if="showInfo">
      <cpi-info v-if="inflationType !== InflationType.General"></cpi-info>
      <inflation-info v-else></inflation-info>
    </template>
  </div>
</template>

<script setup lang="ts">
import CpiInfo from './Info/CpiInfo.vue'
import InflationInfo from './Info/InflationInfo.vue'

import { calculatorState } from '@/state/calculatorState'
import { InflationType } from '@/types/InflatitonTypeEnum'
import { showInfo } from '@/state/infoState'
import { trackEvent } from '@/helpers/matomo'

const { inflationType } = calculatorState

const togleInfo = () => {
  showInfo.value = !showInfo.value
  trackEvent('Calculator', 'Toggle Detail')
}
</script>