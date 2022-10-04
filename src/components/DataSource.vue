<template>
  <div class="footer">
    <p class="text-sm">Data sources: </p>
    <ul>
      <li v-if="inflationType === InflationType.General">
        <a href="https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=MY"> data.worldbank.org </a> 
        (1960 - 2021),
        estimate (2022)
      </li>
      <li v-else-if="inflationType === InflationType.BigMac">
        <a href="https://data.nasdaq.com/data/ECONOMIST/BIGMAC_MYS-big-mac-index-malaysia"> data.nasdaq.com </a> 
      </li>
      <li v-else>
        data.gov.my
        <a href="https://www.data.gov.my/data/ms_MY/dataset/consumer-price-index-cpi-for-main-groups-peninsular-malaysiasabah-and-sarawak-annual">(2000 - 2005)</a> 
        <a href="https://www.data.gov.my/data/ms_MY/dataset/consumer-price-index-2010-100-index-number-for-main-groups-malaysia-annual">(2005 - 2020)</a> 
        <br />
        <a href="https://newss.statistics.gov.my/newss-portalx/ep/epFreeDownloadContentSearch.seam?cid=13057"> newss.statistics.gov.my (2021 - 2022(AUG))</a>
        <br />
        <a href="https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Finflation-calc.xkre.me%2Fdata%2FCpiDataset.xlsx">Raw data</a>
      </li>
    </ul>
    <p class="text-xs mt-2">Note: somehow data from data.gov.my and newss.statistics.gov.my is different for the same period </p>
    <p class="text-xs mt-2">Disclaimer: This is not a financial advice. Data are from consumer perspective </p>
  </div>
</template>

<script setup lang="ts">
import { calculatorState } from '@/state/calculatorState'
import { InflationType } from '@/types/InflatitonTypeEnum'

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
