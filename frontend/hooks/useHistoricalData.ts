'use client'

import { useState } from 'react'

interface HistoricalDataPoint {
  date: Date
  no2: number
  o3: number
  aqi: number
}

interface HistoricalStats {
  avgNO2: string
  avgO3: string
  maxAQI: string
  dataPoints: string
}

export function useHistoricalData() {
  const [historicalData, setHistoricalData] = useState<HistoricalDataPoint[]>([])
  const [stats, setStats] = useState<HistoricalStats>({
    avgNO2: '--',
    avgO3: '--',
    maxAQI: '--',
    dataPoints: '--'
  })

  const generateHistoricalData = (year?: string, month?: string, days?: string): HistoricalDataPoint[] => {
    const data: HistoricalDataPoint[] = []
    const numDays = parseInt(days || '30')
    
    // If year and month are specified, generate data for that specific month
    let startDate: Date
    if (year && month) {
      startDate = new Date(parseInt(year), parseInt(month) - 1, 1)
      // For specific month, generate data for the entire month
      const daysInMonth = new Date(parseInt(year), parseInt(month), 0).getDate()
      
      for (let i = 0; i < Math.min(daysInMonth, numDays); i++) {
        const date = new Date(startDate)
        date.setDate(date.getDate() + i)
        
        // Generate month-specific patterns
        const dayOfMonth = date.getDate()
        const monthFactor = getMonthlyPollutionFactor(parseInt(month))
        const weekdayFactor = date.getDay() === 0 || date.getDay() === 6 ? 0.8 : 1.2 // Weekend vs weekday
        
        const no2 = (25 + Math.random() * 35) * monthFactor * weekdayFactor
        const o3 = (35 + Math.random() * 25) * (2 - monthFactor) * (date.getHours() > 12 ? 1.3 : 0.9)
        const aqi = Math.round(Math.max(no2 * 2, o3 * 1.5))
        
        data.push({ date, no2, o3, aqi })
      }
    } else {
      // Generate data for the last N days from current date
      const now = new Date()
      for (let i = numDays; i >= 0; i--) {
        const date = new Date(now)
        date.setDate(date.getDate() - i)
        
        // Generate realistic seasonal and daily patterns
        const dayOfYear = Math.floor((date.getTime() - new Date(date.getFullYear(), 0, 0).getTime()) / (1000 * 60 * 60 * 24))
        const seasonalFactor = 1 + 0.3 * Math.sin((dayOfYear / 365) * 2 * Math.PI)
        
        const no2 = (30 + Math.random() * 40) * seasonalFactor
        const o3 = (40 + Math.random() * 30) * (2 - seasonalFactor) // O3 inversely related to season
        const aqi = Math.round(Math.max(no2 * 2, o3 * 1.5))
        
        data.push({ date, no2, o3, aqi })
      }
    }
    
    return data
  }

  const getMonthlyPollutionFactor = (month: number): number => {
    // Delhi pollution patterns by month (1-12)
    const monthlyFactors = {
      1: 1.8,  // January - High pollution (winter)
      2: 1.6,  // February - High pollution
      3: 1.3,  // March - Moderate
      4: 1.1,  // April - Moderate
      5: 1.0,  // May - Moderate
      6: 0.9,  // June - Lower (monsoon approaching)
      7: 0.7,  // July - Low (monsoon)
      8: 0.8,  // August - Low (monsoon)
      9: 0.9,  // September - Moderate
      10: 1.4, // October - High (post-monsoon, stubble burning)
      11: 1.7, // November - Very high (stubble burning, winter onset)
      12: 1.9  // December - Highest (winter peak)
    }
    return monthlyFactors[month as keyof typeof monthlyFactors] || 1.0
  }

  const calculateStats = (data: HistoricalDataPoint[]): HistoricalStats => {
    if (data.length === 0) {
      return {
        avgNO2: '--',
        avgO3: '--',
        maxAQI: '--',
        dataPoints: '--'
      }
    }

    const avgNO2 = data.reduce((sum, d) => sum + d.no2, 0) / data.length
    const avgO3 = data.reduce((sum, d) => sum + d.o3, 0) / data.length
    const maxAQI = Math.max(...data.map(d => d.aqi))
    
    return {
      avgNO2: avgNO2.toFixed(1),
      avgO3: avgO3.toFixed(1),
      maxAQI: maxAQI.toString(),
      dataPoints: data.length.toString()
    }
  }

  const loadHistoricalData = async (year?: string, month?: string, days?: string) => {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    try {
      // In a real app, this would be an API call with date parameters
      // const response = await axios.get(`/api/v1/historical?year=${year}&month=${month}&days=${days}`)
      // const data = response.data
      
      console.log(`📅 Loading historical data for: ${month}/${year} (${days} days)`)
      const data = generateHistoricalData(year, month, days)
      setHistoricalData(data)
      setStats(calculateStats(data))
      
      return data
    } catch (error) {
      console.error('Failed to load historical data:', error)
      
      // Generate fallback data
      const fallbackData = generateHistoricalData(year, month, days)
      setHistoricalData(fallbackData)
      setStats(calculateStats(fallbackData))
      
      throw error
    }
  }

  return {
    historicalData,
    stats,
    loadHistoricalData
  }
}