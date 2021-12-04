import { ref } from 'vue'

const url_string = window.location.href
const url = new URL(url_string)

const state = Boolean(Number(url.searchParams.get('s') ?? 0))

export const showInfo = ref(state)
