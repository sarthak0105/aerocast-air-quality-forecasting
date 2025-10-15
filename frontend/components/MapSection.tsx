'use client'

import { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import dynamic from 'next/dynamic'

// Dynamically import the map component to avoid SSR issues
const MapComponent = dynamic(() => import('./Map'), { 
  ssr: false,
  loading: () => (
    <div className="h-96 bg-gray-100 rounded-xl flex items-center justify-center">
      <div className="text-gray-500">Loading map...</div>
    </div>
  )
})

interface MapSectionProps {
  coordinates: { lat: number; lng: number }
  onLocationChange: (lat: number, lng: number) => void
  modelStatus: {
    accuracy: string
    modelName: string
    status: string
  }
}

export function MapSection({ coordinates, onLocationChange, modelStatus }: MapSectionProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'trained_model_active':
        return 'status-good'
      case 'intelligent_fallback':
        return 'status-moderate'
      case 'error':
        return 'status-poor'
      default:
        return 'status-good'
    }
  }

  const getLocationName = (lat: number, lng: number) => {
    // Simple location mapping based on coordinates
    if (Math.abs(lat - 28.6315) < 0.01 && Math.abs(lng - 77.2167) < 0.01) return 'Connaught Place'
    if (Math.abs(lat - 28.6129) < 0.01 && Math.abs(lng - 77.2295) < 0.01) return 'India Gate'
    if (Math.abs(lat - 28.5921) < 0.01 && Math.abs(lng - 77.0460) < 0.01) return 'Dwarka'
    if (Math.abs(lat - 28.4595) < 0.01 && Math.abs(lng - 77.0266) < 0.01) return 'Gurgaon'
    if (Math.abs(lat - 28.5355) < 0.01 && Math.abs(lng - 77.3910) < 0.01) return 'Noida'
    return 'Delhi Center'
  }

  return (
    <div className="p-8 bg-gradient-to-br from-gray-50 to-white border-r border-gray-200/50">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-3">
          <i className="fas fa-map text-blue-600"></i>
          Location Selection
        </h3>

        {/* Map Container */}
        <div className="mb-6">
          <div className="relative rounded-2xl overflow-hidden shadow-xl border-4 border-transparent bg-gradient-to-r from-blue-500 to-purple-600 p-1">
            <div className="bg-white rounded-xl overflow-hidden">
              <MapComponent
                coordinates={coordinates}
                onLocationChange={onLocationChange}
              />
            </div>
          </div>
        </div>

        {/* Current Selection Info */}
        <Card className="mb-4 border-0 shadow-lg bg-gradient-to-r from-blue-500 to-purple-600 text-white">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <i className="fas fa-info-circle"></i>
              Current Selection
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="font-medium">Coordinates:</span>
              <span className="font-mono bg-white/20 px-2 py-1 rounded">
                {coordinates.lat.toFixed(4)}, {coordinates.lng.toFixed(4)}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="font-medium">Location:</span>
              <span>{getLocationName(coordinates.lat, coordinates.lng)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="font-medium">Status:</span>
              <div className="flex items-center gap-2">
                <div className={`w-3 h-3 rounded-full pulse-dot ${getStatusColor(modelStatus.status)}`}></div>
                <span>Ready for forecast</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Model Status Info */}
        <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg text-gray-800">
              <i className="fas fa-brain text-purple-600"></i>
              Model Status
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="font-medium text-gray-700">Model:</span>
              <span className="text-gray-900">{modelStatus.modelName}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="font-medium text-gray-700">Accuracy:</span>
              <span className="font-bold text-blue-600">{modelStatus.accuracy}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="font-medium text-gray-700">Status:</span>
              <div className="flex items-center gap-2">
                <div className={`w-3 h-3 rounded-full pulse-dot ${getStatusColor(modelStatus.status)}`}></div>
                <span className="text-gray-900">
                  {modelStatus.status === 'trained_model_active' ? 'Active' :
                   modelStatus.status === 'intelligent_fallback' ? 'Fallback' :
                   modelStatus.status === 'error' ? 'Error' : 'Ready'}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}