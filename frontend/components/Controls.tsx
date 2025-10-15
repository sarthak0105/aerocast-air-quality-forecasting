'use client'

import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'

interface ControlsProps {
  coordinates: { lat: number; lng: number }
  forecastHours: number
  onCoordinatesChange: (lat: number, lng: number) => void
  onForecastHoursChange: (hours: number) => void
  onGetForecast: () => void
  isLoading: boolean
}

export function Controls({
  coordinates,
  forecastHours,
  onCoordinatesChange,
  onForecastHoursChange,
  onGetForecast,
  isLoading
}: ControlsProps) {
  const quickLocations = [
    { value: '28.6315,77.2167', label: '🏢 Connaught Place' },
    { value: '28.6129,77.2295', label: '🏛️ India Gate' },
    { value: '28.5921,77.0460', label: '🏘️ Dwarka' },
    { value: '28.4595,77.0266', label: '🏙️ Gurgaon' },
    { value: '28.5355,77.3910', label: '🌆 Noida' },
  ]

  const handleLocationPresetChange = (value: string) => {
    if (value) {
      const [lat, lng] = value.split(',').map(Number)
      onCoordinatesChange(lat, lng)
    }
  }

  return (
    <div className="gradient-secondary border-b border-gray-200/50 p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          {/* Latitude */}
          <div className="space-y-2">
            <Label htmlFor="latitude" className="flex items-center gap-2 font-semibold text-gray-700">
              <i className="fas fa-map-marker-alt text-blue-600"></i>
              Latitude
            </Label>
            <Input
              id="latitude"
              type="number"
              value={coordinates.lat}
              onChange={(e) => onCoordinatesChange(Number(e.target.value), coordinates.lng)}
              step="0.0001"
              min="28.4"
              max="28.9"
              className="border-2 border-gray-200 focus:border-blue-500 rounded-xl transition-all duration-300"
            />
          </div>

          {/* Longitude */}
          <div className="space-y-2">
            <Label htmlFor="longitude" className="flex items-center gap-2 font-semibold text-gray-700">
              <i className="fas fa-map-marker-alt text-blue-600"></i>
              Longitude
            </Label>
            <Input
              id="longitude"
              type="number"
              value={coordinates.lng}
              onChange={(e) => onCoordinatesChange(coordinates.lat, Number(e.target.value))}
              step="0.0001"
              min="76.8"
              max="77.5"
              className="border-2 border-gray-200 focus:border-blue-500 rounded-xl transition-all duration-300"
            />
          </div>

          {/* Forecast Hours */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2 font-semibold text-gray-700">
              <i className="fas fa-clock text-blue-600"></i>
              Forecast Hours
            </Label>
            <Select value={forecastHours.toString()} onValueChange={(value) => onForecastHoursChange(Number(value))}>
              <SelectTrigger className="border-2 border-gray-200 focus:border-blue-500 rounded-xl">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="12">12 hours</SelectItem>
                <SelectItem value="24">24 hours</SelectItem>
                <SelectItem value="48">48 hours</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Quick Locations */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2 font-semibold text-gray-700">
              <i className="fas fa-location-dot text-blue-600"></i>
              Quick Locations
            </Label>
            <Select onValueChange={handleLocationPresetChange}>
              <SelectTrigger className="border-2 border-gray-200 focus:border-blue-500 rounded-xl">
                <SelectValue placeholder="Select location..." />
              </SelectTrigger>
              <SelectContent>
                {quickLocations.map((location) => (
                  <SelectItem key={location.value} value={location.value}>
                    {location.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Get Forecast Button */}
        <div className="text-center space-y-4">
          <Button
            onClick={onGetForecast}
            disabled={isLoading}
            className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-8 py-4 rounded-full font-semibold text-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            {isLoading ? (
              <>
                <LoadingSpinner size="sm" className="mr-2" />
                Generating...
              </>
            ) : (
              <>
                <i className="fas fa-chart-line mr-2"></i>
                Get Forecast
              </>
            )}
          </Button>
          
          {/* Debug Info */}
          <div className="text-xs text-gray-500 bg-gray-100 p-2 rounded">
            API: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'} | 
            Location: {coordinates.lat.toFixed(4)}, {coordinates.lng.toFixed(4)} | 
            Hours: {forecastHours}
          </div>
        </div>
      </motion.div>
    </div>
  )
}