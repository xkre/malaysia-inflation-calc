export const trackEvent = (category: string, action: string, name?: string) => {
  var tracker = window._paq
  
  if (!name)
    tracker.push(['trackEvent', category, action])
  else
    tracker.push(['trackEvent', category, action, name])
}