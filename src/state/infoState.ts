import { ref } from 'vue'
import { getQueryParam } from '@/services/routeService'

const state = Boolean(Number(getQueryParam('s') ?? 0))

export const showInfo = ref(state)
