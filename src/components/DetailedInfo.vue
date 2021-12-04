<template>
  <div class="flex flex-col">
    <button class="text-blue-500" @click="show = !show"> {{ show ? 'Hide' : 'More'}} Info </button>
    <template v-if="show">
      <cpi-info v-if="inflationType !== InflationType.General"></cpi-info>
      <inflation-info v-else></inflation-info>
    </template>
  </div>
</template>

<script setup lang="ts">
import CpiInfo from './Info/CpiInfo.vue'
import InflationInfo from './Info/InflationInfo.vue'

import { ref } from '@vue/reactivity'
import { calculatorState } from '../state/calculatorState'
import { InflationType } from '../types/InflatitonTypeEnum'

const { inflationType } = calculatorState
const show = ref(true)
</script>