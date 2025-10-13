import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import MiniTrend from "@/components/aero/mini-trend"

const locations = [
  { id: 1, name: "Connaught Place", city: "Delhi", aqi: 118 },
  { id: 2, name: "Rohini", city: "Delhi", aqi: 103 },
  { id: 3, name: "Okhla", city: "Delhi", aqi: 126 },
  { id: 4, name: "Dwarka", city: "Delhi", aqi: 97 },
]

export default function LocationsPage() {
  return (
    <div className="space-y-6">
      <section className="flex items-center justify-between">
        <h2 className="text-lg font-medium">Saved Locations</h2>
        <div className="flex items-center gap-2">
          <Button variant="secondary">Compare</Button>
          <Button>Add Location</Button>
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {locations.map((loc) => (
          <Card key={loc.id} className="hover:shadow-sm transition-shadow">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm">{loc.name}</CardTitle>
              <p className="text-xs text-muted-foreground">{loc.city}</p>
            </CardHeader>
            <CardContent className="flex items-center justify-between">
              <div className="text-2xl font-semibold">{loc.aqi}</div>
              <MiniTrend />
            </CardContent>
          </Card>
        ))}
      </section>
    </div>
  )
}
