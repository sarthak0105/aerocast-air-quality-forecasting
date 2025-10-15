'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Header } from '@/components/Header'
import { StatsBar } from '@/components/StatsBar'
import { Controls } from '@/components/Controls'
import { MapSection } from '@/components/MapSection'
import { ChartSection } from '@/components/ChartSection'
import { Footer } from '@/components/Footer'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { useAirQuality } from '@/hooks/useAirQuality'
import { toast } from 'sonner'

export default function Dashboard() {
  const [coordinates, setCoordinates] = useState({ lat: 28.6139, lng: 77.2090 })
  const [forecastHours, setForecastHours] = useState(24)
  const [isLoading, setIsLoading] = useState(false)
  
  const {
    currentAQI,
    modelStatus,
    predictionsCount,
    forecastData,
    getForecast,
    incrementPredictionCount
  } = useAirQuality()

  const handleGetForecast = async () => {
    setIsLoading(true)
    try {
      await getForecast(coordinates.lat, coordinates.lng, forecastHours)
      incrementPredictionCount()
      toast.success('Forecast generated successfully!')
    } catch (error) {
      toast.error('Failed to generate forecast. Please try again.')
      console.error('Forecast error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleLocationChange = (lat: number, lng: number) => {
    setCoordinates({ lat, lng })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-600 to-purple-800 relative overflow-hidden">
      {/* Animated background */}
      <div className="fixed inset-0 background-shift pointer-events-none z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-400/30 via-purple-500/20 to-purple-700/30" />
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-white/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-300/10 rounded-full blur-3xl" />
      </div>

      <motion.div 
        className="relative z-10 max-w-7xl mx-auto glass rounded-3xl overflow-hidden shadow-2xl slide-up"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        {/* Shimmer effect on top border */}
        <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-blue-500 via-purple-600 to-blue-500 bg-[length:200%_100%] shimmer" />

        <Header />
        
        <StatsBar 
          currentAQI={currentAQI}
          modelStatus={modelStatus}
          predictionsCount={predictionsCount}
        />
        
        <Controls
          coordinates={coordinates}
          forecastHours={forecastHours}
          onCoordinatesChange={handleLocationChange}
          onForecastHoursChange={setForecastHours}
          onGetForecast={handleGetForecast}
          isLoading={isLoading}
        />
        
        <div className="grid lg:grid-cols-2 gap-0 min-h-[600px]">
          <MapSection
            coordinates={coordinates}
            onLocationChange={handleLocationChange}
            modelStatus={modelStatus}
          />
          
          <ChartSection
            forecastData={forecastData}
            isLoading={isLoading}
          />
        </div>
        
        <Footer />
      </motion.div>

      {isLoading && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="glass p-8 rounded-2xl">
            <LoadingSpinner size="lg" />
            <p className="mt-4 text-center text-gray-700">Generating forecast...</p>
          </div>
        </div>
      )}
    </div>
  )
}