'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Header } from '@/components/Header'
import { Footer } from '@/components/Footer'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { PerformanceChart } from '@/components/charts/PerformanceChart'
import { AccuracyChart } from '@/components/charts/AccuracyChart'
import { LocationChart } from '@/components/charts/LocationChart'
import { HourlyChart } from '@/components/charts/HourlyChart'
import { ErrorChart } from '@/components/charts/ErrorChart'
import { UsageChart } from '@/components/charts/UsageChart'
import { useAnalytics } from '@/hooks/useAnalytics'

export default function AnalyticsPage() {
  const [isLoading, setIsLoading] = useState(true)
  const { analyticsData, loadAnalytics } = useAnalytics()

  useEffect(() => {
    const initializeAnalytics = async () => {
      setIsLoading(true)
      try {
        await loadAnalytics()
      } catch (error) {
        console.error('Analytics loading error:', error)
      } finally {
        setIsLoading(false)
      }
    }

    const timer = setTimeout(initializeAnalytics, 500)
    return () => clearTimeout(timer)
  }, [])

  const performanceMetrics = [
    { label: 'Model Accuracy', value: '95.2%', trend: 'up' },
    { label: 'RMSE Score', value: '12.3', trend: 'up' },
    { label: 'MAE Score', value: '8.7', trend: 'up' },
    { label: 'Predictions Made', value: '1,247', trend: 'neutral' },
    { label: 'System Uptime', value: '99.8%', trend: 'up' },
    { label: 'Avg Response Time', value: '0.8s', trend: 'neutral' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-600 to-purple-800 relative overflow-hidden p-5">
      {/* Animated background */}
      <div className="fixed inset-0 background-shift pointer-events-none z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-400/30 via-purple-500/20 to-purple-700/30" />
      </div>

      <motion.div 
        className="relative z-10 max-w-7xl mx-auto glass rounded-3xl overflow-hidden shadow-2xl slide-up"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Header currentPage="analytics" />
        
        <div className="p-8">
          {/* Performance Metrics Grid */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
            {performanceMetrics.map((metric, index) => (
              <motion.div
                key={metric.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="text-center border-0 shadow-lg bg-white/90 backdrop-blur-sm hover:shadow-xl transition-all duration-300">
                  <CardContent className="p-4">
                    <div className={`text-2xl font-bold mb-2 ${
                      metric.trend === 'up' ? 'text-green-600' : 
                      metric.trend === 'down' ? 'text-red-600' : 
                      'text-blue-600'
                    }`}>
                      {metric.value}
                    </div>
                    <div className="text-xs text-gray-600 font-medium">
                      {metric.label}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Analytics Charts Grid */}
          <div className="grid lg:grid-cols-2 gap-8">
            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-gray-800 font-bold text-lg">
                  <i className="fas fa-target text-blue-600"></i>
                  Model Performance
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-full">
                      <LoadingSpinner size="lg" />
                    </div>
                  ) : (
                    <PerformanceChart data={analyticsData?.performance} />
                  )}
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-gray-800 font-bold text-lg">
                  <i className="fas fa-chart-area text-green-600"></i>
                  Prediction Accuracy Over Time
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-full">
                      <LoadingSpinner size="lg" />
                    </div>
                  ) : (
                    <AccuracyChart data={analyticsData?.accuracy} />
                  )}
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-gray-800 font-bold text-lg">
                  <i className="fas fa-map-marked-alt text-purple-600"></i>
                  Location-wise Performance
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-full">
                      <LoadingSpinner size="lg" />
                    </div>
                  ) : (
                    <LocationChart data={analyticsData?.locations} />
                  )}
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-gray-800 font-bold text-lg">
                  <i className="fas fa-clock text-orange-600"></i>
                  Hourly Prediction Patterns
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-full">
                      <LoadingSpinner size="lg" />
                    </div>
                  ) : (
                    <HourlyChart data={analyticsData?.hourly} />
                  )}
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-gray-800 font-bold text-lg">
                  <i className="fas fa-exclamation-triangle text-red-600"></i>
                  Error Distribution
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-full">
                      <LoadingSpinner size="lg" />
                    </div>
                  ) : (
                    <ErrorChart data={analyticsData?.errors} />
                  )}
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-gray-800 font-bold text-lg">
                  <i className="fas fa-users text-indigo-600"></i>
                  API Usage Statistics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center mb-4">
                  <div className="text-4xl font-bold text-blue-600 mb-2">2,847</div>
                  <div className="text-sm text-gray-600">Total API calls this month</div>
                </div>
                <div className="h-64">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-full">
                      <LoadingSpinner size="lg" />
                    </div>
                  ) : (
                    <UsageChart data={analyticsData?.usage} />
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
        
        <Footer />
      </motion.div>
    </div>
  )
}