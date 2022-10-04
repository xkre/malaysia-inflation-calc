import { RouteState } from "@/types/route"

type routeKeys = `${keyof RouteState}`

const url_string = window.location.href
const url = new URL(url_string)

export const getQueryParam = (param: routeKeys) => {
  return url.searchParams.get(param)
}
