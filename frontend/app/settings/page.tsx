'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Header } from '@/components/Header'
import { Footer } from '@/components/Footer'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Switch } from '@/components/ui/switch'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useSettings } from '@/hooks/useSettings'
import { toast } from 'sonner'

export default function SettingsPage() {
  const { settings, updateSettings, resetSettings, clearData } = useSettings()
  const [showSuccess, setShowSuccess] = useState(false)

  const handleSaveSettings = () => {
    updateSettings(settings)
    setShowSuccess(true)
    toast.success('Settings saved successfully!')
    setTimeout(() => setShowSuccess(false), 3000)
  }

  const handleResetSettings = () => {
    if (confirm('Are you sure you want to reset all settings to defaults?')) {
      resetSettings()
      toast.success('Settings reset to defaults')
    }
  }

  const handleClearData = () => {
    if (confirm('Are you sure you want to clear all cached data? This action cannot be undone.')) {
      clearData()
      toast.success('All data cleared successfully')
    }
  }

  const settingSections = [
    {
      title: 'Notifications',
      icon: 'fas fa-bell',
      items: [
        {
          label: 'Air Quality Alerts',
          description: 'Receive notifications when air quality reaches unhealthy levels',
          type: 'switch',
          key: 'notifications.airQualityAlerts'
        },
        {
          label: 'Daily Forecast',
          description: 'Get daily air quality forecast summary',
          type: 'switch',
          key: 'notifications.dailyForecast'
        },
        {
          label: 'Model Updates',
          description: 'Notifications about model improvements and updates',
          type: 'switch',
          key: 'notifications.modelUpdates'
        }
      ]
    },
    {
      title: 'Display Preferences',
      icon: 'fas fa-display',
      items: [
        {
          label: 'Units',
          description: 'Choose measurement units for pollutant concentrations',
          type: 'select',
          key: 'display.units',
          options: [
            { value: 'ugm3', label: 'μg/m³' },
            { value: 'ppm', label: 'ppm' },
            { value: 'ppb', label: 'ppb' }
          ]
        },
        {
          label: 'Default Forecast Hours',
          description: 'Default time horizon for forecasts',
          type: 'select',
          key: 'display.defaultHours',
          options: [
            { value: '12', label: '12 hours' },
            { value: '24', label: '24 hours' },
            { value: '48', label: '48 hours' }
          ]
        },
        {
          label: 'Chart Type',
          description: 'Preferred chart style for forecasts',
          type: 'select',
          key: 'display.chartType',
          options: [
            { value: 'line', label: 'Line Chart' },
            { value: 'area', label: 'Area Chart' },
            { value: 'bar', label: 'Bar Chart' }
          ]
        },
        {
          label: 'Auto-refresh',
          description: 'Automatically refresh forecasts',
          type: 'switch',
          key: 'display.autoRefresh'
        }
      ]
    },
    {
      title: 'Location Settings',
      icon: 'fas fa-map-marker-alt',
      items: [
        {
          label: 'Default Location',
          description: 'Your preferred location for forecasts',
          type: 'select',
          key: 'location.defaultLocation',
          options: [
            { value: '28.6315,77.2167', label: 'Connaught Place' },
            { value: '28.6129,77.2295', label: 'India Gate' },
            { value: '28.5921,77.0460', label: 'Dwarka' },
            { value: '28.4595,77.0266', label: 'Gurgaon' },
            { value: '28.5355,77.3910', label: 'Noida' }
          ]
        },
        {
          label: 'Location Tracking',
          description: 'Use your current location for forecasts',
          type: 'switch',
          key: 'location.locationTracking'
        }
      ]
    },
    {
      title: 'API Configuration',
      icon: 'fas fa-key',
      items: [
        {
          label: 'API Endpoint',
          description: 'Custom API endpoint URL',
          type: 'input',
          key: 'api.endpoint'
        },
        {
          label: 'Request Timeout',
          description: 'API request timeout in seconds',
          type: 'number',
          key: 'api.timeout'
        },
        {
          label: 'Cache Duration',
          description: 'How long to cache forecast data (minutes)',
          type: 'number',
          key: 'api.cacheDuration'
        }
      ]
    },
    {
      title: 'Data Management',
      icon: 'fas fa-database',
      items: [
        {
          label: 'Export Format',
          description: 'Preferred format for data exports',
          type: 'select',
          key: 'data.exportFormat',
          options: [
            { value: 'json', label: 'JSON' },
            { value: 'csv', label: 'CSV' },
            { value: 'xlsx', label: 'Excel' }
          ]
        },
        {
          label: 'Data Retention',
          description: 'How long to keep historical data locally',
          type: 'select',
          key: 'data.retention',
          options: [
            { value: '7', label: '7 days' },
            { value: '30', label: '30 days' },
            { value: '90', label: '90 days' },
            { value: '365', label: '1 year' }
          ]
        }
      ]
    }
  ]

  const getNestedValue = (obj: any, path: string) => {
    return path.split('.').reduce((current, key) => current?.[key], obj)
  }

  const setNestedValue = (obj: any, path: string, value: any) => {
    const keys = path.split('.')
    const lastKey = keys.pop()!
    const target = keys.reduce((current, key) => {
      if (!current[key]) current[key] = {}
      return current[key]
    }, obj)
    target[lastKey] = value
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-600 to-purple-800 relative overflow-hidden p-5">
      {/* Animated background */}
      <div className="fixed inset-0 background-shift pointer-events-none z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-400/30 via-purple-500/20 to-purple-700/30" />
      </div>

      <motion.div 
        className="relative z-10 max-w-4xl mx-auto glass rounded-3xl overflow-hidden shadow-2xl slide-up"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Header currentPage="settings" />
        
        <div className="p-8">
          {showSuccess && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 p-4 bg-green-100 border border-green-300 text-green-700 rounded-lg flex items-center gap-2"
            >
              <i className="fas fa-check-circle"></i>
              Settings saved successfully!
            </motion.div>
          )}

          <div className="space-y-8">
            {settingSections.map((section, sectionIndex) => (
              <motion.div
                key={section.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: sectionIndex * 0.1 }}
              >
                <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <i className={`${section.icon} text-blue-600`}></i>
                      {section.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {section.items.map((item, itemIndex) => (
                      <div key={item.key} className="flex items-center justify-between py-3 border-b border-gray-100 last:border-b-0">
                        <div className="flex-1">
                          <Label className="font-semibold text-gray-700">
                            {item.label}
                          </Label>
                          <p className="text-sm text-gray-500 mt-1">
                            {item.description}
                          </p>
                        </div>
                        <div className="ml-6">
                          {item.type === 'switch' && (
                            <Switch
                              checked={getNestedValue(settings, item.key) || false}
                              onCheckedChange={(checked) => {
                                const newSettings = { ...settings }
                                setNestedValue(newSettings, item.key, checked)
                                updateSettings(newSettings)
                              }}
                            />
                          )}
                          {item.type === 'select' && (
                            <Select
                              value={getNestedValue(settings, item.key) || ''}
                              onValueChange={(value) => {
                                const newSettings = { ...settings }
                                setNestedValue(newSettings, item.key, value)
                                updateSettings(newSettings)
                              }}
                            >
                              <SelectTrigger className="w-40">
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent>
                                {item.options?.map((option) => (
                                  <SelectItem key={option.value} value={option.value}>
                                    {option.label}
                                  </SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                          )}
                          {(item.type === 'input' || item.type === 'number') && (
                            <Input
                              type={item.type === 'number' ? 'number' : 'text'}
                              value={getNestedValue(settings, item.key) || ''}
                              onChange={(e) => {
                                const newSettings = { ...settings }
                                const value = item.type === 'number' ? 
                                  parseInt(e.target.value) || 0 : 
                                  e.target.value
                                setNestedValue(newSettings, item.key, value)
                                updateSettings(newSettings)
                              }}
                              className="w-40"
                            />
                          )}
                        </div>
                      </div>
                    ))}
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Action Buttons */}
          <div className="flex justify-center gap-4 mt-8 pt-8 border-t border-gray-200">
            <Button 
              onClick={handleSaveSettings}
              className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-8 py-3 rounded-full font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
            >
              <i className="fas fa-save mr-2"></i>
              Save Settings
            </Button>
            
            <Button 
              onClick={handleResetSettings}
              variant="outline"
              className="px-8 py-3 rounded-full font-semibold border-2 hover:bg-gray-50 transition-all duration-300"
            >
              <i className="fas fa-undo mr-2"></i>
              Reset to Defaults
            </Button>
            
            <Button 
              onClick={handleClearData}
              variant="destructive"
              className="px-8 py-3 rounded-full font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
            >
              <i className="fas fa-trash mr-2"></i>
              Clear All Data
            </Button>
          </div>
        </div>
        
        <Footer />
      </motion.div>
    </div>
  )
}