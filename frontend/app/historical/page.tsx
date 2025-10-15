'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Header } from '@/components/Header'
import { Footer } from '@/components/Footer'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
// import { Label } from '@/components/ui/label'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { HistoricalChart } from '@/components/charts/HistoricalChart'
import { MonthlyChart } from '@/components/charts/MonthlyChart'
import { AQIDistributionChart } from '@/components/charts/AQIDistributionChart'
import { useHistoricalData } from '@/hooks/useHistoricalData'
import { toast } from 'sonner'
import { Label } from '@/components/ui/label'
import { Label } from '@/components/ui/label'
import { Select } from '@/components/ui/select'
import { SelectContent } from '@/components/ui/select'
import { SelectItem } from '@/components/ui/select'
import { SelectItem } from '@/components/ui/select'
import { SelectContent } from '@/components/ui/select'
import { SelectTrigger } from '@/components/ui/select'
import { SelectValue } from '@/components/ui/select'
import { SelectTrigger } from '@/components/ui/select'
import { Select } from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { Label } from '@/components/ui/label'
import { Select } from '@/components/ui/select'
import { SelectContent } from '@/components/ui/select'
import { SelectItem } from '@/components/ui/select'
import { SelectItem } from '@/components/ui/select'
import { SelectContent } from '@/components/ui/select'
import { SelectTrigger } from '@/components/ui/select'
import { SelectValue } from '@/components/ui/select'
import { SelectTrigger } from '@/components/ui/select'
import { Select } from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { Label } from '@/components/ui/label'
import { Select } from '@/components/ui/select'
import { SelectContent } from '@/components/ui/select'
import { SelectItem } from '@/components/ui/select'
import { SelectItem } from '@/components/ui/select'
import { SelectContent } from '@/components/ui/select'
import { SelectTrigger } from '@/components/ui/select'
import { SelectValue } from '@/components/ui/select'
import { SelectTrigger } from '@/components/ui/select'
import { Select } from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { Label } from '@/components/ui/label'

export default function HistoricalPage() {
  const [isLoading, setIsLoading] = useState(false)
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear().toString())
  const [selectedMonth, setSelectedMonth] = useState((new Date().getMonth() + 1).toString())
  const [dateRange, setDateRange] = useState('30') // days
  
  const { 
    historicalData, 
    stats, 
    loadHistoricalData 
  } = useHistoricalData()

  const handleLoadData = async () => {
    setIsLoading(true)
    try {
      await loadHistoricalData(selectedYear, selectedMonth, dateRange)
      toast.success('Historical data loaded successfully!')
    } catch (error) {
      toast.error('Failed to load historical data')
      console.error('Historical data error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Generate year options (last 5 years)
  const currentYear = new Date().getFullYear()
  const yearOptions = Array.from({ length: 5 }, (_, i) => currentYear - i)
  
  // Month options
  const monthOptions = [
    { value: '1', label: 'January' },
    { value: '2', label: 'February' },
    { value: '3', label: 'March' },
    { value: '4', label: 'April' },
    { value: '5', label: 'May' },
    { value: '6', label: 'June' },
    { value: '7', label: 'July' },
    { value: '8', label: 'August' },
    { value: '9', label: 'September' },
    { value: '10', label: 'October' },
    { value: '11', label: 'November' },
    { value: '12', label: 'December' }
  ]

  // Date range options
  const rangeOptions = [
    { value: '7', label: 'Last 7 days' },
    { value: '30', label: 'Last 30 days' },
    { value: '90', label: 'Last 3 months' },
    { value: '365', label: 'Last year' }
  ]

  useEffect(() => {
    // Auto-load data on page load
    const timer = setTimeout(() => {
      handleLoadData()
    }, 500)
    return () => clearTimeout(timer)
  }, [])

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
        <Header currentPage="historical" />
        
        <div className="p-8">
          {/* Date Filter Controls */}
          <Card className="mb-8 border-0 shadow-lg bg-white/90 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <i className="fas fa-calendar-alt text-blue-600"></i>
                Data Filter Options
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
                <div className="space-y-2">
                  <Label htmlFor="year-select" className="text-sm font-semibold text-gray-700">
                    <i className="fas fa-calendar mr-2"></i>Year
                  </Label>
                  <Select value={selectedYear} onValueChange={setSelectedYear}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select year" />
                    </SelectTrigger>
                    <SelectContent>
                      {yearOptions.map((year) => (
                        <SelectItem key={year} value={year.toString()}>
                          {year}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="month-select" className="text-sm font-semibold text-gray-700">
                    <i className="fas fa-calendar-days mr-2"></i>Month
                  </Label>
                  <Select value={selectedMonth} onValueChange={setSelectedMonth}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select month" />
                    </SelectTrigger>
                    <SelectContent>
                      {monthOptions.map((month) => (
                        <SelectItem key={month.value} value={month.value}>
                          {month.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="range-select" className="text-sm font-semibold text-gray-700">
                    <i className="fas fa-clock mr-2"></i>Date Range
                  </Label>
                  <Select value={dateRange} onValueChange={setDateRange}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select range" />
                    </SelectTrigger>
                    <SelectContent>
                      {rangeOptions.map((range) => (
                        <SelectItem key={range.value} value={range.value}>
                          {range.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label className="text-sm font-semibold text-gray-700">
                    <i className="fas fa-download mr-2"></i>Load Data
                  </Label>
                  <Button 
                    onClick={handleLoadData}
                    disabled={isLoading}
                    className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
                  >
                    {isLoading ? (
                      <>
                        <LoadingSpinner size="sm" className="mr-2" />
                        Loading...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-search mr-2"></i>
                        Load Data
                      </>
                    )}
                  </Button>
                </div>
              </div>

              {/* Selected Filter Summary */}
              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <div className="flex items-center gap-2 text-blue-800">
                  <i className="fas fa-info-circle"></i>
                  <span className="font-semibold">Current Filter:</span>
                  <span>
                    {monthOptions.find(m => m.value === selectedMonth)?.label} {selectedYear} 
                    ({rangeOptions.find(r => r.value === dateRange)?.label})
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Stats Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
            <Card className="text-center border-0 shadow-lg bg-white/90 backdrop-blur-sm hover:shadow-xl transition-all duration-300">
              <CardContent className="p-6">
                <div className="text-3xl font-bold text-blue-600 mb-2">
                  {stats.avgNO2 || '--'}
                </div>
                <div className="text-sm text-gray-600">Avg NO2 (μg/m³)</div>
                <div className="text-xs text-gray-400 mt-1">
                  {monthOptions.find(m => m.value === selectedMonth)?.label} {selectedYear}
                </div>
              </CardContent>
            </Card>
            
            <Card className="text-center border-0 shadow-lg bg-white/90 backdrop-blur-sm hover:shadow-xl transition-all duration-300">
              <CardContent className="p-6">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {stats.avgO3 || '--'}
                </div>
                <div className="text-sm text-gray-600">Avg O3 (μg/m³)</div>
                <div className="text-xs text-gray-400 mt-1">
                  {monthOptions.find(m => m.value === selectedMonth)?.label} {selectedYear}
                </div>
              </CardContent>
            </Card>
            
            <Card className="text-center border-0 shadow-lg bg-white/90 backdrop-blur-sm hover:shadow-xl transition-all duration-300">
              <CardContent className="p-6">
                <div className="text-3xl font-bold text-red-600 mb-2">
                  {stats.maxAQI || '--'}
                </div>
                <div className="text-sm text-gray-600">Max AQI</div>
                <div className="text-xs text-gray-400 mt-1">
                  Peak value
                </div>
              </CardContent>
            </Card>
            
            <Card className="text-center border-0 shadow-lg bg-white/90 backdrop-blur-sm hover:shadow-xl transition-all duration-300">
              <CardContent className="p-6">
                <div className="text-3xl font-bold text-purple-600 mb-2">
                  {stats.dataPoints || '--'}
                </div>
                <div className="text-sm text-gray-600">Data Points</div>
                <div className="text-xs text-gray-400 mt-1">
                  {rangeOptions.find(r => r.value === dateRange)?.label}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Charts */}
          <div className="space-y-8">
            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <i className="fas fa-chart-line text-blue-600"></i>
                  Time Series Analysis
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-96">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-full">
                      <LoadingSpinner size="lg" />
                    </div>
                  ) : (
                    <HistoricalChart data={historicalData} />
                  )}
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <i className="fas fa-calendar-alt text-green-600"></i>
                  Monthly Averages
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-96">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-full">
                      <LoadingSpinner size="lg" />
                    </div>
                  ) : (
                    <MonthlyChart data={historicalData} />
                  )}
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <i className="fas fa-chart-pie text-purple-600"></i>
                  AQI Distribution
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-96">
                  {isLoading ? (
                    <div className="flex items-center justify-center h-full">
                      <LoadingSpinner size="lg" />
                    </div>
                  ) : (
                    <AQIDistributionChart data={historicalData} />
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