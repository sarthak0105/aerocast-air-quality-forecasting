import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function AboutPage() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle>How It Works</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm leading-relaxed">
          <p>
            Aero Cast is a front-end platform designed to visualize, forecast, and analyze air quality in megacities.
          </p>
          <p>
            It focuses on Nitrogen Dioxide (NO₂) and Ozone (O₃) metrics, presenting trends, alerts, and insights using a
            clean, data-first interface.
          </p>
          <p className="text-muted-foreground">
            This demo uses placeholder components and charts, ready for future integration with real data sources.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Data Sources</CardTitle>
        </CardHeader>
        <CardContent className="text-sm">
          <ul className="list-disc pl-5 space-y-1">
            <li>Government air quality monitoring networks</li>
            <li>Open environmental datasets and APIs</li>
            <li>Satellite-based observations (future)</li>
          </ul>
        </CardContent>
      </Card>

      <Card className="lg:col-span-3">
        <CardHeader>
          <CardTitle>Contact</CardTitle>
        </CardHeader>
        <CardContent className="text-sm">
          <p>For support or inquiries, please reach out via the project page on Vercel.</p>
        </CardContent>
      </Card>
    </div>
  )
}
