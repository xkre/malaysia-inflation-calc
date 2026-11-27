<template>
  <div
    v-if="points.length > 0"
    class="rounded-md border border-gray-200 bg-gray-50/60 p-3.5 space-y-2.5"
  >
    <!-- Header & Live Hover Readout -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1.5">
      <div class="flex items-center gap-2">
        <span class="text-xs font-semibold uppercase tracking-wider text-gray-500">
          Value Progression
        </span>
        <span class="text-xs text-gray-400">
          {{ getPointLabel(points[0]) }} – {{ getPointLabel(points[points.length - 1]) }}
        </span>
      </div>

      <div v-if="activePoint" class="flex flex-wrap items-baseline gap-x-2 gap-y-0.5 text-sm">
        <span class="font-semibold text-gray-700 tabular-nums">
          {{ getPointLabel(activePoint) }}:
        </span>
        <span class="font-semibold text-blue-600 tabular-nums">
          RM {{ formatRmFull(activePoint.value) }}
        </span>
        <span v-if="activeMetricText" class="text-xs text-gray-500 tabular-nums">
          ({{ activeMetricText }})
        </span>
      </div>
    </div>

    <!-- Single-Period Fallback -->
    <p v-if="points.length === 1" class="text-xs text-gray-500 py-4 text-center">
      Select two different periods to view progression over time.
    </p>

    <!-- SVG Line Chart -->
    <div v-else class="w-full">
      <svg
        ref="svgRef"
        :viewBox="`0 0 ${SVG_WIDTH} ${SVG_HEIGHT}`"
        class="w-full h-auto select-none touch-pan-y overflow-visible"
        role="img"
        :aria-label="`Equivalent RM progression from ${getPointLabel(points[0])} to ${getPointLabel(points[points.length - 1])}`"
      >
        <defs>
          <linearGradient :id="gradientId" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#2757FF" stop-opacity="0.16" />
            <stop offset="100%" stop-color="#2757FF" stop-opacity="0.0" />
          </linearGradient>
        </defs>

        <!-- Horizontal Dashed Gridlines & Y-Axis Labels -->
        <g v-for="tick in yTicks" :key="tick.label + tick.y">
          <line
            :x1="MARGIN.left"
            :x2="SVG_WIDTH - MARGIN.right"
            :y1="tick.y"
            :y2="tick.y"
            stroke="#E5E7EB"
            stroke-width="1"
            stroke-dasharray="3 3"
          />
          <text
            :x="MARGIN.left - 8"
            :y="tick.y + 3.5"
            text-anchor="end"
            class="fill-gray-500 text-[10px] tabular-nums"
          >
            {{ tick.label }}
          </text>
        </g>

        <!-- Area Fill -->
        <path :d="areaPath" :fill="`url(#${gradientId})`" />

        <!-- Line Series -->
        <polyline
          :points="polylinePoints"
          fill="none"
          stroke="#2757FF"
          stroke-width="2.25"
          stroke-linecap="round"
          stroke-linejoin="round"
        />

        <!-- Static Markers (all points when <= 16, otherwise endpoints only) -->
        <circle
          v-for="(marker, idx) in staticMarkers"
          :key="`${getPointKey(marker)}-${idx}`"
          :cx="marker.x"
          :cy="marker.y"
          :r="points.length <= 16 ? 2.75 : 3"
          fill="#ffffff"
          stroke="#2757FF"
          stroke-width="1.75"
        />

        <!-- Active Scrub Guide & Highlight Dot -->
        <line
          v-if="isHovering && activeCoord"
          :x1="activeCoord.x"
          :x2="activeCoord.x"
          :y1="MARGIN.top"
          :y2="SVG_HEIGHT - MARGIN.bottom"
          stroke="#93C5FD"
          stroke-width="1"
          stroke-dasharray="3 3"
        />
        <circle
          v-if="activeCoord"
          :cx="activeCoord.x"
          :cy="activeCoord.y"
          r="4.5"
          fill="#2757FF"
          stroke="#ffffff"
          stroke-width="2"
        />

        <!-- X-Axis Period Labels -->
        <text
          v-for="(tick, idx) in xTicks"
          :key="`${tick.label}-${idx}`"
          :x="tick.x"
          :y="SVG_HEIGHT - 6"
          :text-anchor="tick.anchor"
          class="fill-gray-500 text-[10px] tabular-nums"
        >
          {{ tick.label }}
        </text>

        <!-- Interactive Pointer Overlay -->
        <rect
          :x="MARGIN.left"
          :y="MARGIN.top"
          :width="PLOT_WIDTH"
          :height="PLOT_HEIGHT"
          fill="transparent"
          class="cursor-crosshair"
          @mousemove="onMouseMove"
          @mouseleave="clearHover"
          @touchstart.passive="onTouchMove"
          @touchmove.passive="onTouchMove"
          @touchend="clearHover"
        />
      </svg>
    </div>
  </div>
</template>

<script lang="ts">
let chartSeq = 0
</script>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { ChartPoint } from '@/types/chart'

const props = defineProps<{
  points: ChartPoint[]
  year1?: number
  year2?: number
  targetKey?: string | number
  metricLabel: string
  metricFormat: 'index' | 'rm' | 'pct'
  metricDecimals?: number
}>()

const SVG_WIDTH = 560
const SVG_HEIGHT = 205
const MARGIN = { top: 14, right: 16, bottom: 26, left: 60 }
const PLOT_WIDTH = SVG_WIDTH - MARGIN.left - MARGIN.right
const PLOT_HEIGHT = SVG_HEIGHT - MARGIN.top - MARGIN.bottom

const gradientId = `inflation-line-grad-${++chartSeq}`
const svgRef = ref<SVGSVGElement | null>(null)
const activeIndex = ref<number | null>(null)

const isHovering = computed(() => activeIndex.value !== null)

const getPointKey = (p: ChartPoint): string | number => p.key ?? p.year ?? ''
const getPointLabel = (p: ChartPoint): string =>
  p.label ?? String(p.year ?? p.key ?? '')
const getPointTickLabel = (p: ChartPoint): string =>
  p.tickLabel ?? getPointLabel(p)

const defaultIndex = computed(() => {
  const target = props.targetKey ?? props.year2
  if (target !== undefined) {
    const targetIdx = props.points.findIndex((p) => getPointKey(p) === target)
    if (targetIdx >= 0) return targetIdx
  }
  return Math.max(0, props.points.length - 1)
})

const displayIndex = computed(() => {
  if (
    activeIndex.value !== null &&
    activeIndex.value >= 0 &&
    activeIndex.value < props.points.length
  ) {
    return activeIndex.value
  }
  return defaultIndex.value
})

const activePoint = computed(() => props.points[displayIndex.value] ?? null)

const yBounds = computed(() => {
  const vals = props.points.map((p) => p.value)
  const rawMin = Math.min(...vals)
  const rawMax = Math.max(...vals)
  const span = rawMax - rawMin

  if (span < 1e-9) {
    const pad = Math.max(Math.abs(rawMin) * 0.05, 1)
    const min = rawMin >= 0 && rawMin - pad < 0 ? 0 : rawMin - pad
    return { min, max: rawMax + pad }
  }

  const pad = span * 0.08
  const min = rawMin >= 0 && rawMin - pad < 0 ? 0 : rawMin - pad
  return { min, max: rawMax + pad }
})

const coords = computed(() => {
  const n = props.points.length
  if (n < 2) return []
  const { min, max } = yBounds.value
  const ySpan = max - min || 1

  return props.points.map((p, idx) => {
    const x = MARGIN.left + (idx / (n - 1)) * PLOT_WIDTH
    const y = MARGIN.top + ((max - p.value) / ySpan) * PLOT_HEIGHT
    return { ...p, x, y }
  })
})

const activeCoord = computed(() => coords.value[displayIndex.value] ?? null)

const polylinePoints = computed(() =>
  coords.value.map((c) => `${c.x.toFixed(1)},${c.y.toFixed(1)}`).join(' ')
)

const areaPath = computed(() => {
  const c = coords.value
  if (c.length < 2) return ''
  const bottomY = MARGIN.top + PLOT_HEIGHT
  const linePart = c
    .map((pt) => `${pt.x.toFixed(1)},${pt.y.toFixed(1)}`)
    .join(' L ')
  return `M ${c[0].x.toFixed(1)},${bottomY} L ${linePart} L ${c[c.length - 1].x.toFixed(1)},${bottomY} Z`
})

const staticMarkers = computed(() => {
  const c = coords.value
  if (c.length < 2) return []
  if (c.length <= 16) return c
  return [c[0], c[c.length - 1]]
})

const formatCompactRm = (val: number, span: number): string => {
  const abs = Math.abs(val)
  const sign = val < 0 ? '-' : ''
  if (abs >= 1_000_000) {
    return `${sign}RM ${parseFloat((abs / 1_000_000).toFixed(2))}M`
  }
  if (abs >= 10_000) {
    return `${sign}RM ${parseFloat((abs / 1_000).toFixed(1))}k`
  }
  if (abs >= 1_000) {
    return `${sign}RM ${parseFloat((abs / 1_000).toFixed(2))}k`
  }
  if (span < 10) {
    return `${sign}RM ${abs.toFixed(1)}`
  }
  return `${sign}RM ${Math.round(abs)}`
}

const yTicks = computed(() => {
  const { min, max } = yBounds.value
  const span = max - min
  const steps = 3 // 4 horizontal gridlines
  const result: Array<{ y: number; label: string }> = []

  for (let i = 0; i <= steps; i++) {
    const ratio = i / steps
    const val = max - ratio * span
    const y = MARGIN.top + ratio * PLOT_HEIGHT
    result.push({ y, label: formatCompactRm(val, span) })
  }
  return result
})

const xTicks = computed(() => {
  const c = coords.value
  const n = c.length
  if (n < 2) return []

  let indices: number[]
  if (n <= 5) {
    indices = c.map((_, idx) => idx)
  } else {
    const raw = [0, 1, 2, 3, 4].map((k) => Math.round((k * (n - 1)) / 4))
    indices = Array.from(new Set(raw))
    if (indices.length >= 3) {
      const last = c[indices[indices.length - 1]]
      const prev = c[indices[indices.length - 2]]
      if (last.x - prev.x < 48) {
        indices.splice(indices.length - 2, 1)
      }
    }
  }

  return indices.map((idx, pos) => {
    const pt = c[idx]
    let anchor: 'start' | 'middle' | 'end' = 'middle'
    if (pos === 0) anchor = 'start'
    else if (pos === indices.length - 1) anchor = 'end'
    return { label: getPointTickLabel(pt), x: pt.x, anchor }
  })
})

const formatRmFull = (val: number): string =>
  val.toLocaleString('en-MY', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })

const activeMetricText = computed(() => {
  const pt = activePoint.value
  if (!pt || pt.metric === undefined) return ''

  if (props.metricFormat === 'rm') {
    return `${props.metricLabel} RM ${pt.metric.toFixed(2)}`
  }
  if (props.metricFormat === 'pct') {
    const sign = pt.metric > 0 ? '+' : ''
    return `${props.metricLabel} ${sign}${pt.metric.toFixed(2)}%`
  }
  const formatted =
    props.metricDecimals !== undefined
      ? pt.metric.toFixed(props.metricDecimals)
      : String(pt.metric)
  return `${props.metricLabel} ${formatted}`
})

const updateActiveFromClientX = (clientX: number) => {
  const svg = svgRef.value
  const n = props.points.length
  if (!svg || n < 2) return

  const rect = svg.getBoundingClientRect()
  if (rect.width <= 0) return

  const svgX = ((clientX - rect.left) / rect.width) * SVG_WIDTH
  const ratio = Math.max(0, Math.min(1, (svgX - MARGIN.left) / PLOT_WIDTH))
  activeIndex.value = Math.round(ratio * (n - 1))
}

const onMouseMove = (event: MouseEvent) => {
  updateActiveFromClientX(event.clientX)
}

const onTouchMove = (event: TouchEvent) => {
  if (event.touches.length > 0) {
    updateActiveFromClientX(event.touches[0].clientX)
  }
}

const clearHover = () => {
  activeIndex.value = null
}
</script>
