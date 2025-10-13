"use client"
import { ResponsiveContainer, AreaChart, Area } from "recharts"

const demo = [
  { x: 1, y: 30 },
  { x: 2, y: 33 },
  { x: 3, y: 29 },
  { x: 4, y: 35 },
  { x: 5, y: 32 },
  { x: 6, y: 31 },
]

export default function MiniTrend() {
  return (
    <div className="h-10 w-24">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={demo}>
          <Area dataKey="y" stroke="var(--chart-3)" fill="var(--chart-3)" fillOpacity={0.2} strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
