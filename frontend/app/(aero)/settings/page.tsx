"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useState } from "react"

export default function SettingsPage() {
  const [notifications, setNotifications] = useState(true)

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <Card>
        <CardHeader>
          <CardTitle>Units & Range</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-2">
            <Label htmlFor="units">Units</Label>
            <Select defaultValue="ugm3">
              <SelectTrigger id="units">
                <SelectValue placeholder="Select units" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ugm3">µg/m³</SelectItem>
                <SelectItem value="ppm">ppm</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid gap-2">
            <Label htmlFor="range">Forecast Range</Label>
            <Select defaultValue="24h">
              <SelectTrigger id="range">
                <SelectValue placeholder="Select range" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="24h">Next 24 hours</SelectItem>
                <SelectItem value="48h">Next 48 hours</SelectItem>
                <SelectItem value="7d">Next 7 days</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Preferences</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <Label htmlFor="notifs">Notifications</Label>
            <Switch id="notifs" checked={notifications} onCheckedChange={setNotifications} aria-label="Notifications" />
          </div>
          <div className="flex items-center justify-between">
            <Label htmlFor="theme">High Contrast Mode</Label>
            <Switch id="theme" />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
