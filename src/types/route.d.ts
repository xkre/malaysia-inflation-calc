import { InflationType } from "./InflatitonTypeEnum";
import { MalaysiaPart } from "./malaysiaPartEnum";

export type RouteState = {
  y1: number;
  y2: number;
  v1: number;
  i: InflationType;
  p: MalaysiaPart;
  s: number;
}
