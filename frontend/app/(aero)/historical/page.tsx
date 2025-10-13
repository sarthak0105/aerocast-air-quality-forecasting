"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import PlaceholderChart from "@/components/aero/placeholder-chart"
import { Calendar } from "lucide-react"

export default function HistoricalPage() {
  return (
    <div className="space-y-6">
      <section className="flex flex-col md:flex-row items-start md:items-center gap-3">
        <div className="flex items-center gap-2">
          <Button variant="outline">
            <Calendar className="h-4 w-4 mr-2" />
            Start Date
          </Button>
          <Button variant="outline">
            <Calendar className="h-4 w-4 mr-2" />
            End Date
          </Button>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <Button variant="secondary">Compare NO₂ vs O₃</Button>
          <Button>Export CSV</Button>
        </div>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>NO₂ – Historical Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <PlaceholderChart height={260} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>O₃ – Historical Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <PlaceholderChart height={260} />
          </CardContent>
        </Card>
      </section>
    </div>
  )
}
