'use client'

import { useState, useEffect } from 'react'

interface Settings {
  notifications: {
    airQualityAlerts: boolean
    dailyForecast: boolean
    modelUpdates: boolean
  }
  display: {
    units: string
    defaultHours: string
    chartType: string
    autoRefresh: boolean
  }
  location: {
    defaultLocation: string
    locationTracking: boolean
  }
  api: {
    endpoint: string
    timeout: number
    cacheDuration: number
  }
  data: {
    exportFormat: string
    retention: string
  }
}

const defaultSettings: Settings = {
  notifications: {
    airQualityAlerts: true,
    dailyForecast: false,
    modelUpdates: true
  },
  display: {
    units: 'ugm3',
    defaultHours: '24',
    chartType: 'line',
    autoRefresh: true
  },
  location: {
    defaultLocation: '28.6129,77.2295',
    locationTracking: false
  },
  api: {
    endpoint: 'http://localhost:8000/api/v1',
    timeout: 10,
    cacheDuration: 15
  },
  data: {
    exportFormat: 'json',
    retention: '30'
  }
}

export function useSettings() {
  const [settings, setSettings] = useState<Settings>(defaultSettings)

  // Load settings from localStorage on mount
  useEffect(() => {
    const savedSettings = localStorage.getItem('airQualitySettings')
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings)
        setSettings({ ...defaultSettings, ...parsed })
      } catch (error) {
        console.error('Error loading settings:', error)
      }
    }
  }, [])

  const updateSettings = (newSettings: Settings) => {
    setSettings(newSettings)
    localStorage.setItem('airQualitySettings', JSON.stringify(newSettings))
  }

  const resetSettings = () => {
    setSettings(defaultSettings)
    localStorage.removeItem('airQualitySettings')
  }

  const clearData = () => {
    // Clear all localStorage data
    localStorage.clear()
    
    // Clear any cached API responses
    if ('caches' in window) {
      caches.keys().then(names => {
        names.forEach(name => {
          caches.delete(name)
        })
      })
    }
  }

  return {
    settings,
    updateSettings,
    resetSettings,
    clearData
  }
}