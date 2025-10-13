import MetricCard from "@/components/aero/metric-card"
import PlaceholderChart from "@/components/aero/placeholder-chart"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function Page() {
  return (
    <div className="space-y-6">
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <MetricCard title="NO₂ (Now)" value={58} unit="µg/m³" badge="Moderate" badgeTone="highlight" />
        <MetricCard title="O₃ (Now)" value={32} unit="µg/m³" badge="Stable" badgeTone="accent" />
        <MetricCard title="AQI (Composite)" value={112} badge="Watch" badgeTone="secondary" />
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="text-pretty">Today’s Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <PlaceholderChart />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-pretty">Forecast Summary</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-sm text-muted-foreground">
              Expect a midday NO₂ peak with gradual decline into evening. O₃ rising into afternoon hours.
            </p>
            <ul className="text-sm list-disc pl-5 space-y-1">
              <li>NO₂ peak around 09:00–12:00</li>
              <li>O₃ moderate increase into afternoon</li>
              <li>Light winds; dispersion improving by night</li>
            </ul>
            <Button variant="default" className="w-full">
              View Full Forecast
            </Button>
          </CardContent>
        </Card>
      </section>
    </div>
  )
}
