import { 
  cpiMalaysia, 
  cpiSabahLabuan, 
  cpiSarawak, 
  cpiSemenanjung, 
  inflation 
} from "../assets/data"
import { InflationType } from "../types/InflatitonTypeEnum"

export const getYearlyInflation = (year1: number, year2: number): YearlyInflation[] => {
  const smaller = year1 < year2 ? year1 : year2
  const larger = year1 > year2 ? year1 : year2

  if (smaller < 1959) throw 'No Data'
  if (larger > 2021) throw 'No Data'

  const inflationYear = Object.keys(inflation)
    .map(x => Number(x))
    .filter(x => x > smaller && x <= larger)
    .map(x => ({
      year: x,
      inflation: inflation[x]
    }))

  return inflationYear
}

export const getCumulativeInflation = (year1: number, year2: number): number => {
  if (year1 === year2) return 1

  const yearlyInflation = getYearlyInflation(year1, year2)

  if (yearlyInflation.length === 0) {
    throw 'No data'
  }

  console.debug({ inflation })
  console.debug({ yearlyInflation, length: yearlyInflation.length })

  let cumulInflation = 1

  if (year2 > year1) {
    for (const yearInflation of yearlyInflation) {
      const rate = yearInflation.inflation

      cumulInflation = cumulInflation + rate * cumulInflation / 100
    }
  } else {
    yearlyInflation.reverse()

    for (const yearInflation of yearlyInflation) {
      const rate = yearInflation.inflation

      cumulInflation = cumulInflation - rate * cumulInflation / 100
    }
  }

  console.debug(`Cumulative inflation from ${year1} to ${year2}:`, cumulInflation)

  return cumulInflation
}

export const getCPI = (year1: number, year2: number, type: InflationType): number => {
  if (type === InflationType.General)
    throw 'Error'

  const cpiData = cpiSemenanjung

  const year1Cpi = cpiData[year1]?.[type]
  const year2Cpi = cpiData[year2]?.[type]

  if (year1Cpi === undefined || year2Cpi === undefined)
    throw 'No Data'

  const relativePrice = year2Cpi / year1Cpi

  console.debug({ year1Cpi, year2Cpi, relativePrice })

  return relativePrice
}

// export const getFoodCPI = (year1: number, year2: number): number => {
//   const year1Cpi = cpiData[year1]?.food
//   const year2Cpi = cpiData[year2]?.food

//   if (year1Cpi === undefined || year2Cpi === undefined)
//     throw 'No Data'

//   return year2Cpi / year1Cpi
// }
