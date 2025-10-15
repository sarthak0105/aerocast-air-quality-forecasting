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

interface UsageChartProps {
  data?: {
    labels: string[]
    values: number[]
  }
}

export function UsageChart({ data }: UsageChartProps) {
  if (!data) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        No usage data available
      </div>
    )
  }

  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: 'API Calls',
        data: data.values,
        backgroundColor: 'rgba(102, 126, 234, 0.7)',
        borderColor: '#667eea',
        borderWidth: 1
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'API Calls'
        }
      }
    }
  }

  return <Bar data={chartData} options={options} />
}