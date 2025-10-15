'use client'

import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { ForecastChart } from '@/components/charts/ForecastChart'
import { AirQualityCard } from '@/components/AirQualityCard'

interface ChartSectionProps {
  forecastData: any
  isLoading: boolean
}

export function ChartSection({ forecastData, isLoading }: ChartSectionProps) {
  return (
    <div className="p-8 bg-gradient-to-br from-white to-gray-50">
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-3">
          <i className="fas fa-chart-area text-purple-600"></i>
          Air Quality Forecast
        </h3>

        <div id="forecast-content">
          {isLoading ? (
            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardContent className="p-12">
                <div className="text-center">
                  <LoadingSpinner size="lg" className="mb-4" />
                  <div className="text-gray-600 text-lg">Generating forecast...</div>
                </div>
              </CardContent>
            </Card>
          ) : forecastData ? (
            <div className="space-y-6">
              {/* Forecast Chart */}
              <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm chart-container">
                <CardContent className="p-6">
                  <div className="h-80">
                    <ForecastChart data={forecastData} />
                  </div>
                </CardContent>
              </Card>

              {/* Air Quality Cards */}
              <div className="grid gap-4">
                {forecastData.predictions && forecastData.predictions.length > 0 && (
                  <>
                    <AirQualityCard
                      pollutant="NO2"
                      value={forecastData.predictions[0].no2}
                      unit="μg/m³"
                      trend="stable"
                      status="moderate"
                    />
                    <AirQualityCard
                      pollutant="O3"
                      value={forecastData.predictions[0].o3}
                      unit="μg/m³"
                      trend="increasing"
                      status="good"
                    />
                  </>
                )}
              </div>
            </div>
          ) : (
            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardContent className="p-12">
                <div className="text-center text-gray-600">
                  <i className="fas fa-chart-line text-6xl text-gray-300 mb-4"></i>
                  <div className="text-lg">Click "Get Forecast" to load predictions</div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </motion.div>
    </div>
  )
}