"use client"

import { useState, useEffect } from "react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useLocations } from "@/hooks/use-forecast"
import { MapPin } from "lucide-react"

interface LocationOption {
  name: string
  latitude: number
  longitude: number
  type: string
}

export default function CitySelector() {
  const { locations, loading } = useLocations()
  const [selectedLocation, setSelectedLocation] = useState<string>("Delhi Center")

  // Default locations if API fails
  const defaultLocations: LocationOption[] = [
    { name: "Delhi Center", latitude: 28.6139, longitude: 77.2090, type: "city" },
    { name: "Connaught Place", latitude: 28.6315, longitude: 77.2167, type: "commercial" },
    { name: "India Gate", latitude: 28.6129, longitude: 77.2295, type: "monument" },
    { name: "Dwarka", latitude: 28.5921, longitude: 77.0460, type: "residential" },
    { name: "Gurgaon", latitude: 28.4595, longitude: 77.0266, type: "commercial" },
    { name: "Noida", latitude: 28.5355, longitude: 77.3910, type: "residential" },
  ]

  const availableLocations = locations.length > 0 ? locations : defaultLocations

  const getLocationIcon = (type: string) => {
    switch (type) {
      case 'commercial': return '🏢'
      case 'residential': return '🏘️'
      case 'monument': return '🏛️'
      case 'city': return '🌆'
      default: return '📍'
    }
  }

  return (
    <div className="min-w-[200px]">
      <Select 
        value={selectedLocation} 
        onValueChange={setSelectedLocation}
        disabled={loading}
      >
        <SelectTrigger aria-label="Select location" className="gap-2">
          <MapPin className="h-4 w-4 opacity-70" />
          <SelectValue placeholder={loading ? "Loading..." : "Select location"} />
        </SelectTrigger>
        <SelectContent>
          {availableLocations.map((location) => (
            <SelectItem key={location.name} value={location.name}>
              <div className="flex items-center gap-2">
                <span>{getLocationIcon(location.type)}</span>
                <span>{location.name}</span>
                <span className="text-xs text-muted-foreground ml-auto">
                  {location.type}
                </span>
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}
