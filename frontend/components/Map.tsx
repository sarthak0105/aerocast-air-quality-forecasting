'use client'

import { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

interface MapProps {
  coordinates: { lat: number; lng: number }
  onLocationChange: (lat: number, lng: number) => void
}

export default function Map({ coordinates, onLocationChange }: MapProps) {
  const mapRef = useRef<L.Map | null>(null)
  const markerRef = useRef<L.Marker | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current) return

    // Initialize map
    if (!mapRef.current) {
      mapRef.current = L.map(containerRef.current).setView([coordinates.lat, coordinates.lng], 10)

      // Add tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(mapRef.current)

      // Custom marker icon
      const customIcon = L.divIcon({
        className: 'custom-marker',
        html: '<i class="fas fa-map-marker-alt" style="color: #667eea; font-size: 24px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);"></i>',
        iconSize: [24, 24],
        iconAnchor: [12, 24]
      })

      // Add initial marker
      markerRef.current = L.marker([coordinates.lat, coordinates.lng], { icon: customIcon })
        .addTo(mapRef.current)

      // Handle map clicks
      mapRef.current.on('click', (e: L.LeafletMouseEvent) => {
        const { lat, lng } = e.latlng
        onLocationChange(Number(lat.toFixed(4)), Number(lng.toFixed(4)))
      })
    }

    return () => {
      if (mapRef.current) {
        mapRef.current.remove()
        mapRef.current = null
      }
    }
  }, [])

  // Update marker position when coordinates change
  useEffect(() => {
    if (mapRef.current && markerRef.current) {
      const newLatLng = L.latLng(coordinates.lat, coordinates.lng)
      markerRef.current.setLatLng(newLatLng)
      mapRef.current.setView(newLatLng, mapRef.current.getZoom())
    }
  }, [coordinates])

  return (
    <div 
      ref={containerRef} 
      className="h-96 w-full rounded-xl overflow-hidden"
      style={{ minHeight: '384px' }}
    />
  )
}