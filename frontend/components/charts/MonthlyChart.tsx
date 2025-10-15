'use client'

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Bar } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

interface MonthlyChartProps {
  data: Array<{
    date: Date
    no2: number
    o3: number
    aqi: number
  }>
}

export function MonthlyChart({ data }: MonthlyChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        No data available for monthly analysis
      </div>
    )
  }

  // Group data by month
  const monthData: { [key: string]: { no2: number[]; o3: number[] } } = {}
  
  data.forEach(d => {
    const month = d.date.toLocaleDateString('en-US', { month: 'short' })
    if (!monthData[month]) {
      monthData[month] = { no2: [], o3: [] }
    }
    monthData[month].no2.push(d.no2)
    monthData[month].o3.push(d.o3)
  })

  const months = Object.keys(monthData)
  const avgNO2 = months.map(m => 
    monthData[m].no2.reduce((a, b) => a + b, 0) / monthData[m].no2.length
  )
  const avgO3 = months.map(m => 
    monthData[m].o3.reduce((a, b) => a + b, 0) / monthData[m].o3.length
  )

  const chartData = {
    labels: months,
    datasets: [
      {
        label: 'NO2 Avg',
        data: avgNO2,
        backgroundColor: 'rgba(220, 53, 69, 0.7)',
        borderColor: '#dc3545',
        borderWidth: 1
      },
      {
        label: 'O3 Avg',
        data: avgO3,
        backgroundColor: 'rgba(40, 167, 69, 0.7)',
        borderColor: '#28a745',
        borderWidth: 1
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Average Concentration (μg/m³)'
        }
      }
    }
  }

  return <Bar data={chartData} options={options} />
}