import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function AdminPage() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card>
        <CardHeader>
          <CardTitle>Model Status</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm">
            <strong>Status:</strong> Standby
          </p>
          <p className="text-sm">
            <strong>Last Refresh:</strong> 2h ago
          </p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Data Refresh</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm">
            <strong>Queue:</strong> 0 tasks
          </p>
          <p className="text-sm">
            <strong>Throughput:</strong> —
          </p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>User Metrics</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm">
            <strong>Active Sessions:</strong> 5
          </p>
          <p className="text-sm">
            <strong>Avg. Time:</strong> 3m 12s
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
