<template>
  <div class="flex flex-col">
    <button class="text-blue-500 hover:shadow-inner bg-blue-50 w-80 self-center rounded-sm" @click="togleInfo"> 
      {{ showInfo ? 'Hide' : 'More'}} Info 
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

import { calculatorState } from '../state/calculatorState'
import { InflationType } from '../types/InflatitonTypeEnum'
import { showInfo } from '../state/infoState'
import { trackEvent } from '../helpers/matomo'

const { inflationType } = calculatorState

const togleInfo = () => {
  showInfo.value = !showInfo.value
  trackEvent('Calculator', 'Toggle Detail')
}
</script>