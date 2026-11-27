<template>
  <footer class="container mx-auto px-4 md:px-0 mt-28 pb-10">
    <div class="max-w-screen-sm mx-auto">
      <p class="text-sm font-semibold">Data sources: </p>
      <ul class="text-sm list-disc list-inside space-y-1 mt-1">
        <template v-if="route.name === 'detailed'">
          <li>
            <a target="_blank" href="https://data.gov.my/data-catalogue/cpi_3d" class="underline text-blue-600">CPI by 3-Digit Group (cpi_3d) | data.gov.my</a>
            — 47 groups (2010 - 2026)
          </li>
          <li>
            <a target="_blank" href="https://data.gov.my/data-catalogue/cpi_4d" class="underline text-blue-600">CPI by 4-Digit Class (cpi_4d) | data.gov.my</a>
            — 101 classes (2010 - 2026)
          </li>
          <li>
            <a target="_blank" href="https://data.gov.my/data-catalogue/cpi_5d" class="underline text-blue-600">CPI by 5-Digit Subclass (cpi_5d) | data.gov.my</a>
            — 181 subclasses (2010 - 2026)
          </li>
          <li>
            <a target="_blank" href="https://storage.dosm.gov.my/dictionaries/mcoicop.csv" class="underline text-blue-600">MCOICOP 2018 Classification Dictionary | OpenDOSM</a>
            — 343 categories (EN / BM)
          </li>
          <li>
            <a target="_blank" href="https://open.dosm.gov.my/publications?page=1&pub_type=cpi" class="underline text-blue-600">Consumer Price Index Publications | OpenDOSM</a>
            — Official monthly press releases &amp; bulletins
          </li>
        </template>
        <template v-else-if="inflationType === InflationType.General">
          <li>
            <a target="_blank" href="https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=MY" class="underline text-blue-600">data.worldbank.org</a>
            (1960 - 2025)
          </li>
          <li>
            <a target="_blank" href="https://open.dosm.gov.my/data-catalogue/cpi_annual" class="underline text-blue-600">Annual CPI by Division (2-digit) | OpenDOSM</a>
            (1960 - 2025)
          </li>
          <li>
            <a target="_blank" href="https://open.dosm.gov.my/publications?page=1&pub_type=cpi" class="underline text-blue-600">Consumer Price Index Publications | OpenDOSM</a>
            (Official reports & bulletins)
          </li>
        </template>
        <template v-else-if="inflationType === InflationType.BigMac">
          <li>
            <a target="_blank" href="https://github.com/TheEconomist/big-mac-data" class="underline text-blue-600">The Economist — Big Mac Index (GitHub)</a>
            — Malaysia mid-year / July prices (2000 - 2026)
          </li>
          <li>
            <a target="_blank"
              href="https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Finflation-calc.xkre.me%2Fdata%2FCpiDataset.xlsx" class="underline text-blue-600">Downloadable CpiDataset.xlsx</a>
          </li>
        </template>
        <template v-else>
          <li>
            <a target="_blank" href="https://open.dosm.gov.my/data-catalogue/cpi_annual" class="underline text-blue-600">Annual CPI by Division (2-digit) | OpenDOSM</a>
            — National Headline & 13 COICOP categories (1960 - 2025)
          </li>
          <li>
            <a target="_blank" href="https://open.dosm.gov.my/data-catalogue/cpi_state" class="underline text-blue-600">Monthly CPI by State & Division (2-digit) | OpenDOSM</a>
            — 16 Malaysian States & Federal Territories (2010 - 2026)
          </li>
          <li>
            <a target="_blank" href="https://open.dosm.gov.my/publications?page=1&pub_type=cpi" class="underline text-blue-600">Consumer Price Index Publications | OpenDOSM</a>
            — Official monthly press releases, bulletins & annual summaries
          </li>
          <li>
            <a target="_blank"
              href="https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Finflation-calc.xkre.me%2Fdata%2FCpiDataset.xlsx" class="underline text-blue-600">Downloadable CpiDataset.xlsx</a>
          </li>
        </template>
      </ul>
      <p class="text-sm mt-3 text-gray-500">Note: Official Consumer Price Index (CPI) datasets published by the Department of Statistics Malaysia (DOSM / Jabatan Perangkaan Malaysia).</p>
      <p class="text-sm mt-1 text-gray-500">Disclaimer: This is not financial advice. Data are provided for consumer purchasing power reference.</p>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { calculatorState } from '@/state/calculatorState'
import { InflationType } from '@/types/InflatitonTypeEnum'

const route = useRoute()
const { inflationType } = calculatorState
</script>
