import { RouteState } from "@/types/route"

type routeKeys = `${keyof RouteState}`

export const getQueryParam = (param: routeKeys | string) => {
  return new URLSearchParams(window.location.search).get(param)
}
