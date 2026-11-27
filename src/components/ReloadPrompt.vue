<template>
  <div
    v-if="needRefresh"
    role="alert"
    aria-live="polite"
    class="fixed bottom-4 right-4 z-50 max-w-sm rounded-md border border-gray-200 bg-white p-4 shadow-lg"
  >
    <p class="text-sm text-gray-700">
      New version available. Reload to get the latest data and updates.
    </p>
    <div class="mt-3 flex justify-end space-x-2">
      <button
        type="button"
        @click="updateServiceWorker(true)"
        class="rounded-md bg-blue-500 px-3 py-1.5 text-sm font-medium text-white hover:bg-blue-600"
      >
        Reload
      </button>
      <button
        type="button"
        @click="needRefresh = false"
        class="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
      >
        Dismiss
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount } from 'vue'
import { useRegisterSW } from 'virtual:pwa-register/vue'

let intervalId: number | undefined
let visibilityHandler: (() => void) | undefined

const { needRefresh, updateServiceWorker } = useRegisterSW({
  immediate: true,
  onRegisteredSW(swUrl, registration) {
    if (!registration) return

    const checkForUpdate = async () => {
      if ('connection' in navigator && !navigator.onLine) return
      if (registration.installing) return

      try {
        const resp = await fetch(swUrl, {
          cache: 'no-store',
          headers: {
            cache: 'no-store',
            'cache-control': 'no-cache',
          },
        })

        if (resp.status === 200) {
          await registration.update()
        }
      } catch {
        // Ignore transient network errors during update checks
      }
    }

    // Bypass GitHub Pages HTTP cache on initial registration
    checkForUpdate()

    visibilityHandler = () => {
      if (document.visibilityState === 'visible') {
        checkForUpdate()
      }
    }
    document.addEventListener('visibilitychange', visibilityHandler)

    intervalId = window.setInterval(checkForUpdate, 60 * 60 * 1000)
  },
})

onBeforeUnmount(() => {
  if (visibilityHandler) {
    document.removeEventListener('visibilitychange', visibilityHandler)
  }
  if (intervalId !== undefined) {
    window.clearInterval(intervalId)
  }
})
</script>
