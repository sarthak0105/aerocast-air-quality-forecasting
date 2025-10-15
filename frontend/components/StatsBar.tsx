'use client'

import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'

interface StatsBarProps {
  currentAQI: number | null
  modelStatus: {
    accuracy: string
    modelName: string
    status: string
  }
  predictionsCount: number
}

export function StatsBar({ currentAQI, modelStatus, predictionsCount }: StatsBarProps) {
  const [lastUpdated, setLastUpdated] = useState<string>('')

  useEffect(() => {
    const updateTime = () => {
      const now = new Date()
      setLastUpdated(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }))
    }
    
    updateTime()
    const interval = setInterval(updateTime, 60000) // Update every minute
    
    return () => clearInterval(interval)
  }, [])

  const stats = [
    {
      label: 'Current AQI',
      value: currentAQI?.toString() || '--',
      icon: 'fas fa-wind'
    },
    {
      label: 'Model Accuracy',
      value: modelStatus.accuracy,
      icon: 'fas fa-target'
    },
    {
      label: 'Model Type',
      value: modelStatus.modelName || 'LSTM',
      icon: 'fas fa-brain'
    },
    {
      label: 'Predictions Made',
      value: predictionsCount.toLocaleString(),
      icon: 'fas fa-chart-line'
    },
    {
      label: 'Last Updated',
      value: lastUpdated,
      icon: 'fas fa-clock'
    }
  ]

  return (
    <div className="gradient-secondary border-b border-gray-200/50 py-6 px-4">
      <div className="flex flex-wrap justify-center gap-4 md:gap-8">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.label}
            className="text-center min-w-[120px] p-4 rounded-xl bg-white/50 backdrop-blur-sm shadow-sm hover:shadow-md hover:transform hover:scale-105 transition-all duration-300"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            whileHover={{ y: -2 }}
          >
            {/* Top accent line */}
            <div className="w-8 h-1 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mx-auto mb-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            
            <div className="flex items-center justify-center mb-2">
              <i className={`${stat.icon} text-blue-600 mr-2`}></i>
            </div>
            
            <div className="text-2xl md:text-3xl font-bold gradient-text mb-1">
              {stat.value}
            </div>
            
            <div className="text-xs md:text-sm text-gray-600 font-semibold uppercase tracking-wide">
              {stat.label}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}