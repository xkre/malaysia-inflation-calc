export const trackEvent = (category: string, action: string, name?: string) => {
  const tracker = window._paq
  if (!tracker) return

  if (!name)
    tracker.push(['trackEvent', category, action])
  else
    tracker.push(['trackEvent', category, action, name])
}