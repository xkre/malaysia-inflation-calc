<template>
  <cpi-info v-if="inflationType !== InflationType.General"></cpi-info>
  <inflation-info v-else></inflation-info>
</template>

<script setup lang="ts">
import CpiInfo from './Info/CpiInfo.vue'
import InflationInfo from './Info/InflationInfo.vue'

import { computed } from '@vue/reactivity'
import { calculatorState } from '../state/calculatorState'
import { InflationType } from '../types/InflatitonTypeEnum'

const { inflationType } = calculatorState
</script>