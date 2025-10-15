'use client'

import { useState } from 'react'

interface AnalyticsData {
  performance: {
    labels: string[]
    values: number[]
  }
  accuracy: {
    labels: string[]
    values: number[]
  }
  locations: {
    labels: string[]
    accuracy: number[]
    predictions: number[]
  }
  hourly: {
    labels: string[]
    no2: number[]
    o3: number[]
  }
  errors: {
    labels: string[]
    values: number[]
  }
  usage: {
    labels: string[]
    values: number[]
  }
}

export function useAnalytics() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null)

  const generateAnalyticsData = (): AnalyticsData => {
    return {
      performance: {
        labels: ['NO2 Accuracy', 'O3 Accuracy', 'Overall RMSE', 'Response Time', 'Uptime'],
        values: [94.5, 96.2, 88.7, 92.1, 99.8]
      },
      accuracy: {
        labels: Array.from({length: 30}, (_, i) => {
          const date = new Date()
          date.setDate(date.getDate() - (29 - i))
          return date.toLocaleDateString('en-US', {month: 'short', day: 'numeric'})
        }),
        values: Array.from({length: 30}, () => 90 + Math.random() * 8)
      },
      locations: {
        labels: ['Connaught Place', 'India Gate', 'Dwarka', 'Gurgaon', 'Noida'],
        accuracy: [95.2, 93.8, 94.1, 92.5, 96.1],
        predictions: [245, 198, 167, 223, 189]
      },
      hourly: {
        labels: Array.from({length: 24}, (_, i) => `${i}:00`),
        no2: Array.from({length: 24}, (_, i) => {
          // Higher during rush hours
          const base = 35
          const rushHour = (i >= 7 && i <= 9) || (i >= 17 && i <= 19) ? 15 : 0
          return base + rushHour + Math.random() * 10
        }),
        o3: Array.from({length: 24}, (_, i) => {
          // Higher during afternoon
          const base = 45
          const afternoon = (i >= 12 && i <= 16) ? 20 : 0
          return base + afternoon + Math.random() * 15
        })
      },
      errors: {
        labels: ['< 5 μg/m³', '5-10 μg/m³', '10-15 μg/m³', '15-20 μg/m³', '> 20 μg/m³'],
        values: [45, 30, 15, 7, 3]
      },
      usage: {
        labels: Array.from({length: 7}, (_, i) => {
          const date = new Date()
          date.setDate(date.getDate() - (6 - i))
          return date.toLocaleDateString('en-US', {weekday: 'short'})
        }),
        values: [120, 145, 167, 189, 201, 156, 98]
      }
    }
  }

  const loadAnalytics = async () => {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500))
    
    try {
      // In a real app, this would be an API call
      // const response = await axios.get('/api/v1/analytics')
      // const data = response.data
      
      const data = generateAnalyticsData()
      setAnalyticsData(data)
      
      return data
    } catch (error) {
      console.error('Failed to load analytics data:', error)
      
      // Generate fallback data
      const fallbackData = generateAnalyticsData()
      setAnalyticsData(fallbackData)
      
      throw error
    }
  }

  return {
    analyticsData,
    loadAnalytics
  }
}