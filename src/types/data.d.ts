interface InflationDataset {
  [key: number]: number;
}

interface CPIData extends Record<string, number | undefined> {
  total: number;
  food: number;
  alcoholTobacco?: number;
  clothing: number;
  housing: number;
  furnishing: number;
  health: number;
  transport: number;
  communication: number;
  recreative: number;
  education: number;
  restaurantHotels?: number;
  misc: number;
}

interface CPIDataset {
  [key: number]: CPIData;
}
