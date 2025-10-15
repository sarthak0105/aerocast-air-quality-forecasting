'use client'

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'
import { Doughnut } from 'react-chartjs-2'

ChartJS.register(ArcElement, Tooltip, Legend)

interface AQIDistributionChartProps {
  data: Array<{
    date: Date
    no2: number
    o3: number
    aqi: number
  }>
}

export function AQIDistributionChart({ data }: AQIDistributionChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        No data available for AQI distribution
      </div>
    )
  }

  // Categorize AQI values
  const categories = { 'Good': 0, 'Moderate': 0, 'Unhealthy': 0, 'Very Unhealthy': 0 }
  
  data.forEach(d => {
    if (d.aqi <= 50) categories['Good']++
    else if (d.aqi <= 100) categories['Moderate']++
    else if (d.aqi <= 200) categories['Unhealthy']++
    else categories['Very Unhealthy']++
  })

  const chartData = {
    labels: Object.keys(categories),
    datasets: [
      {
        data: Object.values(categories),
        backgroundColor: [
          '#28a745',
          '#ffc107',
          '#dc3545',
          '#6f42c1'
        ],
        borderWidth: 2,
        borderColor: '#fff'
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const
      }
    }
  }

  return <Doughnut data={chartData} options={options} />
}