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
        data.gov.my
        <a href="https://www.data.gov.my/data/ms_MY/dataset/consumer-price-index-cpi-for-main-groups-peninsular-malaysiasabah-and-sarawak-annual">(2000 - 2005)</a> 
        <a href="https://www.data.gov.my/data/ms_MY/dataset/consumer-price-index-2010-100-index-number-for-main-groups-malaysia-annual">(2005 - 2020)</a> 
        <a href="https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fxkre%2Fmalaysia-inflation-calc%2Fmain%2Fsrc%2Fassets%2Fdata%2FCPI%2520dataset.xlsx">Raw data</a>
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
