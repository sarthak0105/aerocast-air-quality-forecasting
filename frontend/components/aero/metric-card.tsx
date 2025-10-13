"use client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"

export default function MetricCard({
  title,
  value,
  unit,
  badge,
  badgeTone = "accent",
}: {
  title: string
  value: string | number
  unit?: string
  badge?: string
  badgeTone?: "accent" | "highlight" | "secondary"
}) {
  const toneVar =
    badgeTone === "highlight"
      ? "var(--color-highlight)"
      : badgeTone === "secondary"
        ? "var(--secondary)"
        : "var(--accent)"

  const toneFg = badgeTone === "highlight" ? "#0f172a" : badgeTone === "secondary" ? "#ffffff" : "#0f172a"

  return (
    <Card className="hover:shadow-sm transition-shadow">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {badge ? (
          <span
            className={cn("text-xs px-2 py-0.5 rounded")}
            style={{ background: toneVar, color: toneFg }}
            aria-label={`${title} badge`}
          >
            {badge}
          </span>
        ) : null}
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-semibold">
          {value}
          {unit ? <span className="text-sm text-muted-foreground ml-1">{unit}</span> : null}
        </div>
      </CardContent>
    </Card>
  )
}
