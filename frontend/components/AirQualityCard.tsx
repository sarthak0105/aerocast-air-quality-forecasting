'use client'

import { motion } from 'framer-motion'
import { Card, CardContent } from '@/components/ui/card'

interface AirQualityCardProps {
  pollutant: string
  value: number
  unit: string
  trend: 'increasing' | 'decreasing' | 'stable'
  status: 'good' | 'moderate' | 'poor'
}

export function AirQualityCard({ pollutant, value, unit, trend, status }: AirQualityCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'good': return 'text-green-600 border-green-200'
      case 'moderate': return 'text-yellow-600 border-yellow-200'
      case 'poor': return 'text-red-600 border-red-200'
      default: return 'text-gray-600 border-gray-200'
    }
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing': return 'fas fa-arrow-up text-red-500'
      case 'decreasing': return 'fas fa-arrow-down text-green-500'
      case 'stable': return 'fas fa-minus text-gray-500'
      default: return 'fas fa-minus text-gray-500'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4, scale: 1.02 }}
      transition={{ duration: 0.3 }}
    >
      <Card className={`border-l-4 ${getStatusColor(status)} shadow-lg bg-white/90 backdrop-blur-sm hover:shadow-xl transition-all duration-300 overflow-hidden relative`}>
        {/* Shimmer effect */}
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-blue-500/30 to-transparent transform -translate-x-full animate-pulse" />
        
        <CardContent className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h4 className="text-xl font-bold text-gray-800">{pollutant}</h4>
            <div className="flex items-center gap-2">
              <i className={getTrendIcon(trend)}></i>
              <span className="text-sm text-gray-600 capitalize">{trend}</span>
            </div>
          </div>
          
          <div className="flex items-baseline gap-2 mb-2">
            <span className="text-4xl font-bold text-blue-600">
              {value.toFixed(1)}
            </span>
            <span className="text-lg text-gray-600">{unit}</span>
          </div>
          
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${
              status === 'good' ? 'bg-green-500' :
              status === 'moderate' ? 'bg-yellow-500' :
              'bg-red-500'
            } pulse-dot`}></div>
            <span className="text-sm font-medium text-gray-700 capitalize">
              {status} Level
            </span>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}