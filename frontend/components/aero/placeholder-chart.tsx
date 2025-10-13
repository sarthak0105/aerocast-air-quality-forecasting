"use client"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"

const data = [
  { t: "00:00", no2: 42, o3: 20 },
  { t: "03:00", no2: 50, o3: 22 },
  { t: "06:00", no2: 58, o3: 24 },
  { t: "09:00", no2: 70, o3: 29 },
  { t: "12:00", no2: 62, o3: 35 },
  { t: "15:00", no2: 55, o3: 38 },
  { t: "18:00", no2: 60, o3: 32 },
  { t: "21:00", no2: 48, o3: 26 },
]

export default function PlaceholderChart({
  height = 280,
  showLegend = true,
}: {
  height?: number
  showLegend?: boolean
}) {
  return (
    <div style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ left: 8, right: 16, top: 8, bottom: 8 }}>
          <CartesianGrid stroke="var(--muted)" strokeOpacity={0.3} />
          <XAxis dataKey="t" tick={{ fill: "var(--foreground)" }} />
          <YAxis tick={{ fill: "var(--foreground)" }} />
          <Tooltip
            contentStyle={{
              background: "var(--card)",
              color: "var(--foreground)",
              border: "1px solid var(--border)",
            }}
          />
          {showLegend && <Legend />}
          <Line
            type="monotone"
            dataKey="no2"
            name="NO₂"
            stroke="var(--chart-1)"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="o3"
            name="O₃"
            stroke="var(--chart-2)"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
