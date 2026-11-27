<template>
  <div class="space-y-5 mb-7">
    <!-- Quick Search (EN / BM / MCOICOP Code) -->
    <div ref="searchContainerRef" class="relative">
      <label for="mcoicop-search" class="block font-medium text-gray-700">
        Search Category
      </label>
      <div class="relative mt-2">
        <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </span>
        <input
          id="mcoicop-search"
          v-model="searchQuery"
          type="text"
          autocomplete="off"
          placeholder="Search English, BM, or code (e.g. Petrol, Roti, 07222)..."
          @focus="onSearchFocus"
          @input="onSearchInput"
          @keydown.escape="closeDropdown"
          class="block w-full rounded-md border border-gray-300 bg-white py-2 pl-9 pr-9 shadow-sm text-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
        />
        <button
          v-if="searchQuery || isDropdownOpen"
          type="button"
          aria-label="Clear search"
          @click="clearSearch"
          class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Level Filter Pills -->
      <div class="mt-2 flex flex-wrap gap-1.5">
        <button
          v-for="pill in levelFilterPills"
          :key="pill.value"
          type="button"
          @click="setSearchLevel(pill.value)"
          class="px-2.5 py-1 rounded-full text-xs font-medium border transition-colors"
          :class="
            searchLevel === pill.value
              ? 'border-blue-500 bg-blue-50 text-blue-600'
              : 'border-gray-200 bg-white text-gray-600 hover:bg-gray-50'
          "
        >
          {{ pill.label }}
        </button>
      </div>

      <!-- Search Results Dropdown -->
      <div
        v-if="showDropdown"
        class="absolute z-20 mt-1.5 w-full rounded-md border border-gray-200 bg-white shadow-lg overflow-hidden"
      >
        <div v-if="searchResults.length === 0" class="px-4 py-3 text-sm text-gray-500">
          No matching MCOICOP categories found.
        </div>
        <ul v-else class="max-h-72 overflow-y-auto divide-y divide-gray-100">
          <li v-for="item in searchResults" :key="`${item.digits}-${item.code}`">
            <button
              type="button"
              @click="selectFromSearch(item)"
              class="w-full text-left px-3.5 py-2.5 hover:bg-blue-50 focus:bg-blue-50 focus:outline-none transition-colors"
            >
              <div class="flex items-center justify-between gap-2">
                <div class="flex items-center gap-2 min-w-0">
                  <span
                    class="shrink-0 inline-block px-1.5 py-0.5 text-[11px] font-semibold rounded"
                    :class="levelBadgeClass(item.digits)"
                  >
                    {{ LEVEL_LABELS[item.digits] }}
                  </span>
                  <span class="font-mono text-xs font-semibold text-gray-700 shrink-0">
                    <template v-for="(part, idx) in getHighlightParts(item.code)" :key="idx">
                      <mark v-if="part.match" class="bg-yellow-200 text-gray-900 rounded-[2px]">{{ part.text }}</mark>
                      <template v-else>{{ part.text }}</template>
                    </template>
                  </span>
                  <span class="text-sm font-medium text-gray-900 truncate">
                    <template v-for="(part, idx) in getHighlightParts(item.descEn)" :key="idx">
                      <mark v-if="part.match" class="bg-yellow-200 text-gray-900 rounded-[2px]">{{ part.text }}</mark>
                      <template v-else>{{ part.text }}</template>
                    </template>
                  </span>
                </div>
                <span
                  v-if="item.minYear > meta.minYear"
                  class="shrink-0 text-[11px] font-medium px-1.5 py-0.5 rounded bg-amber-50 text-amber-700 border border-amber-200"
                >
                  From {{ item.minYear }}
                </span>
              </div>
              <p
                v-if="hasDistinctBm(item)"
                class="text-xs text-gray-500 mt-0.5 truncate"
              >
                <template v-for="(part, idx) in getHighlightParts(item.descBm)" :key="idx">
                  <mark v-if="part.match" class="bg-yellow-200 text-gray-900 rounded-[2px]">{{ part.text }}</mark>
                  <template v-else>{{ part.text }}</template>
                </template>
              </p>
              <p class="text-[11px] text-gray-400 mt-0.5 truncate">
                {{ formatResultPath(item) }}
              </p>
            </button>
          </li>
        </ul>
        <div
          v-if="searchResults.length > 0"
          class="bg-gray-50 px-3.5 py-1.5 text-[11px] text-gray-500 border-t border-gray-100 flex justify-between items-center"
        >
          <span>Showing {{ searchResults.length }} {{ searchResults.length === 1 ? 'result' : 'results' }}</span>
          <button type="button" @click="closeDropdown" class="text-blue-600 hover:underline">
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Cascading Hierarchy Dropdowns -->
    <div class="space-y-4">
      <div>
        <label for="detailed-division" class="block font-medium text-gray-700">
          Division (Filter)
        </label>
        <select
          id="detailed-division"
          :value="selectedDivision"
          @change="onDivisionChange"
          class="mt-2 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
        >
          <option v-for="div in divisions" :key="div.code" :value="div.code">
            {{ div.code }} · {{ div.descEn }}
          </option>
        </select>
      </div>

      <div>
        <label for="detailed-group" class="block font-medium text-gray-700">
          Group (3-Digit)
        </label>
        <select
          id="detailed-group"
          :value="selectedGroup"
          @change="onGroupChange"
          class="mt-2 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
        >
          <option v-for="grp in groupOptions" :key="grp.code" :value="grp.code">
            {{ grp.code }} · {{ grp.descEn }}
          </option>
        </select>
      </div>

      <div v-if="showClassSelect">
        <label for="detailed-class" class="block font-medium text-gray-700">
          Class (4-Digit) <span class="text-sm font-normal text-gray-400">· Optional</span>
        </label>
        <select
          id="detailed-class"
          :value="selectedClass"
          @change="onClassChange"
          class="mt-2 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
        >
          <option value="">
            All in Group {{ selectedGroup }} (use 3-digit Group)
          </option>
          <option v-for="cls in classOptions" :key="cls.code" :value="cls.code">
            {{ cls.code }} · {{ cls.descEn }}
          </option>
        </select>
      </div>

      <div v-if="showSubclassSelect">
        <label for="detailed-subclass" class="block font-medium text-gray-700">
          Subclass (5-Digit) <span class="text-sm font-normal text-gray-400">· Optional</span>
        </label>
        <select
          id="detailed-subclass"
          :value="selectedSubclass"
          @change="onSubclassChange"
          class="mt-2 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
        >
          <option value="">
            All in Class {{ selectedClass }} (use 4-digit Class)
          </option>
          <option v-for="sub in subclassOptions" :key="sub.code" :value="sub.code">
            {{ sub.code }} · {{ sub.descEn }}
          </option>
        </select>
      </div>

      <p v-if="passthroughNote" class="text-xs text-gray-500">
        {{ passthroughNote }}
      </p>
    </div>

    <!-- Active Selection Summary Banner -->
    <div v-if="activeNode && breadcrumb" class="bg-gray-50 border border-gray-200 rounded-md p-3.5 space-y-1.5">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div class="flex items-center gap-2">
          <span
            class="inline-block px-2 py-0.5 text-xs font-semibold rounded"
            :class="levelBadgeClass(activeNode.digits)"
          >
            {{ LEVEL_LONG_LABELS[activeNode.digits] }}
          </span>
          <span class="font-mono text-xs font-semibold text-gray-700">
            Code {{ activeNode.code }}
          </span>
        </div>
        <span class="text-xs text-gray-500">Malaysia (National)</span>
      </div>

      <div>
        <p class="font-semibold text-gray-900">{{ activeNode.descEn }}</p>
        <p v-if="hasDistinctBm(activeNode)" class="text-xs text-gray-500">
          {{ activeNode.descBm }}
        </p>
      </div>

      <!-- Interactive Breadcrumb -->
      <div class="flex flex-wrap items-center gap-1 text-xs text-gray-500 pt-0.5">
        <span>{{ breadcrumb.division.code }} {{ breadcrumb.division.descEn }}</span>
        <span>›</span>
        <button
          v-if="activeNode.digits > 3"
          type="button"
          @click="selectNodeCode(breadcrumb.group.code)"
          class="text-blue-600 hover:underline text-left"
        >
          {{ breadcrumb.group.code }} {{ breadcrumb.group.descEn }}
        </button>
        <span v-else class="font-medium text-gray-700">
          {{ breadcrumb.group.code }} {{ breadcrumb.group.descEn }}
        </span>

        <template v-if="breadcrumb.classNode">
          <span>›</span>
          <button
            v-if="activeNode.digits > 4"
            type="button"
            @click="selectNodeCode(breadcrumb.classNode.code)"
            class="text-blue-600 hover:underline text-left"
          >
            {{ breadcrumb.classNode.code }} {{ breadcrumb.classNode.descEn }}
          </button>
          <span v-else class="font-medium text-gray-700">
            {{ breadcrumb.classNode.code }} {{ breadcrumb.classNode.descEn }}
          </span>
        </template>

        <template v-if="breadcrumb.subclassNode">
          <span>›</span>
          <span class="font-medium text-gray-700">
            {{ breadcrumb.subclassNode.code }} {{ breadcrumb.subclassNode.descEn }}
          </span>
        </template>
      </div>

      <!-- Availability Range -->
      <p
        class="text-xs pt-0.5"
        :class="activeNode.minYear > meta.minYear ? 'text-amber-700 font-medium' : 'text-gray-500'"
      >
        {{ availabilityText }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { detailedCalculatorState } from '@/state/detailedCalculatorState'
import {
  LEVEL_COUNTS,
  LEVEL_LABELS,
  LEVEL_LONG_LABELS,
  MONTH_NAMES,
  formatYearMonthLabel,
  getAnnualMeta,
  getBreadcrumb,
  getClassesForGroup,
  getDivisionByCode,
  getDivisions,
  getGroupsForDivision,
  getNodeByCode,
  getSubclassesForClass,
  searchMcoicop,
} from '@/services/detailedInflationService'
import { trackEvent } from '@/helpers/matomo'
import type { McoicopLevel, McoicopNode } from '@/types/detailedCpi'

const { selectedCode, granularity } = detailedCalculatorState

const meta = getAnnualMeta()
const divisions = getDivisions()

const searchQuery = ref('')
const searchLevel = ref<McoicopLevel | 'all'>('all')
const isDropdownOpen = ref(false)
const searchContainerRef = ref<HTMLElement | null>(null)

const levelFilterPills: Array<{ value: McoicopLevel | 'all'; label: string }> = [
  { value: 'all', label: `All (${LEVEL_COUNTS.all})` },
  { value: 3, label: `Group · 3D (${LEVEL_COUNTS[3]})` },
  { value: 4, label: `Class · 4D (${LEVEL_COUNTS[4]})` },
  { value: 5, label: `Subclass · 5D (${LEVEL_COUNTS[5]})` },
]

const searchResults = computed(() => {
  const limit = searchQuery.value.trim() ? 50 : 200
  return searchMcoicop(searchQuery.value, searchLevel.value, limit)
})

const showDropdown = computed(() => {
  if (!isDropdownOpen.value) return false
  return searchQuery.value.trim().length > 0 || searchLevel.value !== 'all'
})

const breadcrumb = computed(() => getBreadcrumb(selectedCode.value))
const activeNode = computed(() => getNodeByCode(selectedCode.value))

const selectedDivision = computed(() => breadcrumb.value?.division.code ?? divisions[0]?.code ?? '01')
const selectedGroup = computed(() => breadcrumb.value?.group.code ?? '')
const selectedClass = computed(() => breadcrumb.value?.classNode?.code ?? '')
const selectedSubclass = computed(() => breadcrumb.value?.subclassNode?.code ?? '')

const groupOptions = computed(() => getGroupsForDivision(selectedDivision.value))
const classOptions = computed(() =>
  selectedGroup.value ? getClassesForGroup(selectedGroup.value) : []
)
const subclassOptions = computed(() =>
  selectedClass.value ? getSubclassesForClass(selectedClass.value) : []
)

const showClassSelect = computed(() => {
  const grp = breadcrumb.value?.group
  if (!grp) return false
  return grp.hasDistinctChildren || Boolean(selectedClass.value)
})

const showSubclassSelect = computed(() => {
  const cls = breadcrumb.value?.classNode
  if (!cls) return false
  return cls.hasDistinctChildren || Boolean(selectedSubclass.value)
})

const passthroughNote = computed(() => {
  if (!activeNode.value) return ''
  if (activeNode.value.digits === 3 && !showClassSelect.value) {
    return 'No finer breakdown available under this Group.'
  }
  if (activeNode.value.digits === 4 && !showSubclassSelect.value) {
    return 'No finer breakdown available under this Class.'
  }
  return ''
})

const availabilityText = computed(() => {
  const node = activeNode.value
  if (!node) return ''
  if (granularity.value === 'm') {
    return `Data available: ${formatYearMonthLabel(node.minMonth)} – ${formatYearMonthLabel(node.maxMonth)}`
  }
  const ytdSuffix =
    node.maxYear === meta.ytdYear && meta.ytdMonths < 12
      ? ` (Jan–${MONTH_NAMES[meta.ytdMonths - 1]} YTD)`
      : ''
  return `Data available: ${node.minYear} – ${node.maxYear}${ytdSuffix}`
})

const hasDistinctBm = (node: McoicopNode): boolean =>
  node.descBm.trim().toLowerCase() !== node.descEn.trim().toLowerCase()

const highlightRegex = computed<RegExp | null>(() => {
  const raw = searchQuery.value.trim()
  if (!raw) return null
  const tokens = Array.from(new Set(raw.split(/\s+/).filter(Boolean)))
    .sort((a, b) => b.length - a.length)
    .map((tok) => tok.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))
  if (tokens.length === 0) return null
  return new RegExp(`(${tokens.join('|')})`, 'gi')
})

const getHighlightParts = (
  text: string
): Array<{ text: string; match: boolean }> => {
  const regex = highlightRegex.value
  if (!regex || !text) {
    return [{ text, match: false }]
  }

  const parts: Array<{ text: string; match: boolean }> = []
  regex.lastIndex = 0
  let lastIndex = 0
  let m: RegExpExecArray | null

  while ((m = regex.exec(text)) !== null) {
    if (m[0].length === 0) {
      regex.lastIndex += 1
      continue
    }
    if (m.index > lastIndex) {
      parts.push({ text: text.slice(lastIndex, m.index), match: false })
    }
    parts.push({ text: m[0], match: true })
    lastIndex = m.index + m[0].length
  }

  if (lastIndex < text.length) {
    parts.push({ text: text.slice(lastIndex), match: false })
  }

  return parts.length > 0 ? parts : [{ text, match: false }]
}

const levelBadgeClass = (digits: McoicopLevel): string => {
  if (digits === 3) return 'bg-blue-50 text-blue-700 border border-blue-200'
  if (digits === 4) return 'bg-indigo-50 text-indigo-700 border border-indigo-200'
  return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
}

const formatResultPath = (item: McoicopNode): string => {
  const div = getDivisionByCode(item.division)
  const parts: string[] = []
  if (div) parts.push(`${div.code} ${div.descEn}`)
  if (item.digits >= 4) {
    const grp = getNodeByCode(item.group)
    if (grp) parts.push(`${grp.code} ${grp.descEn}`)
  }
  if (item.digits === 5 && item.classCode) {
    const cls = getNodeByCode(item.classCode)
    if (cls) parts.push(`${cls.code} ${cls.descEn}`)
  }
  return parts.join(' › ')
}

const onSearchFocus = () => {
  if (searchQuery.value.trim().length > 0 || searchLevel.value !== 'all') {
    isDropdownOpen.value = true
  }
}

const onSearchInput = () => {
  isDropdownOpen.value = true
}

const setSearchLevel = (level: McoicopLevel | 'all') => {
  searchLevel.value = level
  if (level !== 'all' || searchQuery.value.trim().length > 0) {
    isDropdownOpen.value = true
  } else {
    isDropdownOpen.value = false
  }
}

const closeDropdown = () => {
  isDropdownOpen.value = false
}

const clearSearch = () => {
  searchQuery.value = ''
  searchLevel.value = 'all'
  isDropdownOpen.value = false
}

const selectFromSearch = (item: McoicopNode) => {
  selectedCode.value = item.code
  clearSearch()
  trackEvent('DetailedCalculator', 'Search Category', item.code)
}

const selectNodeCode = (code: string) => {
  selectedCode.value = code
  trackEvent('DetailedCalculator', 'Select Category', code)
}

const onDivisionChange = (event: Event) => {
  const divCode = (event.target as HTMLSelectElement).value
  const groups = getGroupsForDivision(divCode)
  if (groups.length > 0) {
    selectNodeCode(groups[0].code)
  }
}

const onGroupChange = (event: Event) => {
  const grpCode = (event.target as HTMLSelectElement).value
  if (grpCode) {
    selectNodeCode(grpCode)
  }
}

const onClassChange = (event: Event) => {
  const clsCode = (event.target as HTMLSelectElement).value
  selectNodeCode(clsCode || selectedGroup.value)
}

const onSubclassChange = (event: Event) => {
  const subCode = (event.target as HTMLSelectElement).value
  selectNodeCode(subCode || selectedClass.value)
}

const handleClickOutside = (event: MouseEvent) => {
  if (
    searchContainerRef.value &&
    !searchContainerRef.value.contains(event.target as Node)
  ) {
    isDropdownOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
