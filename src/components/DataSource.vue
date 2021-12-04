<template>
  <div class="footer">
    <p class="text-sm">Data sources: </p>
    <ul>
      <li v-if="inflationType === InflationType.General">
        <a href="https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=MY"> data.worldbank.org </a> 
        (1960 - 2020),
        estimate (2021)
      </li>
      <li v-else>
        <a href="https://www.data.gov.my/data/ms_MY/dataset/consumer-price-index-2010-100-index-number-for-main-groups-malaysia-annual">data.gov.my</a> 
        (2005 - 2020)
      </li>
    </ul>
    <p class="text-xs mt-2">Disclaimer: This is not a financial advice. Data are from consumer perspective </p>
  </div>
</template>

<script setup lang="ts">
import { calculatorState } from '../state/calculatorState'
import { InflationType } from '../types/InflatitonTypeEnum'

const { inflationType } = calculatorState
</script>

<style lang="scss" scoped>
.footer {
  @apply pb-2 text-left;
  margin-top: auto;

  ul {
    @apply text-xs;
  }
}
</style>
