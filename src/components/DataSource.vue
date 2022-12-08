<template>
  <footer class="container mx-auto px-4 md:px-0 mt-28 pb-10">
    <div class="max-w-screen-sm mx-auto">
      <p class="text-sm">Data sources: </p>
      <ul class="text-sm list-disc list-inside">
        <li v-if="inflationType === InflationType.General">
          <a target="_blank" href="https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=MY"> data.worldbank.org </a> 
          (1960 - 2021),
          estimate (2022)
        </li>
        <li v-else-if="inflationType === InflationType.BigMac">
          <a target="_blank" href="https://data.nasdaq.com/data/ECONOMIST/BIGMAC_MYS-big-mac-index-malaysia"> data.nasdaq.com </a> 
        </li>
        <li v-else>
          data.gov.my
          <a target="_blank" href="https://www.data.gov.my/data/ms_MY/dataset/consumer-price-index-cpi-for-main-groups-peninsular-malaysiasabah-and-sarawak-annual">(2000 - 2005)</a> 
          <a target="_blank" href="https://www.data.gov.my/data/ms_MY/dataset/consumer-price-index-2010-100-index-number-for-main-groups-malaysia-annual">(2005 - 2020)</a> 
          <br />
          <a target="_blank" href="https://newss.statistics.gov.my/newss-portalx/ep/epFreeDownloadContentSearch.seam"> newss.statistics.gov.my (2021 - 2022(OCT))</a>
          <br />
          <a target="_blank" href="https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Finflation-calc.xkre.me%2Fdata%2FCpiDataset.xlsx">Raw data</a>
        </li>
      </ul>
      <p class="text-sm mt-2">Note: somehow data from data.gov.my and newss.statistics.gov.my is different for the same period </p>
      <p class="text-sm mt-2">Disclaimer: This is not a financial advice. Data are from consumer perspective </p>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { calculatorState } from '@/state/calculatorState'
import { InflationType } from '@/types/InflatitonTypeEnum'

const { inflationType } = calculatorState
</script>
