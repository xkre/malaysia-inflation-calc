interface Matomo {
  trackPageView(title?: string): void
  trackEvent(category: string, action: string, name?: string, value?: string): void
}

interface Tracker {
  push(params: string []): void
}
