import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import PlaceholderChart from "@/components/aero/placeholder-chart"

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Model Accuracy (Placeholder)</CardTitle>
          </CardHeader>
          <CardContent>
            <PlaceholderChart />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Seasonal Analysis (Placeholder)</CardTitle>
          </CardHeader>
          <CardContent>
            <PlaceholderChart height={240} showLegend={false} />
          </CardContent>
        </Card>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>AQI Trend (Placeholder)</CardTitle>
          </CardHeader>
          <CardContent>
            <PlaceholderChart height={260} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Correlation NO₂ ↔ O₃ (Placeholder)</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Placeholder for correlation matrix or scatter plot between pollutants and weather features.
            </p>
          </CardContent>
        </Card>
      </section>
    </div>
  )
}
