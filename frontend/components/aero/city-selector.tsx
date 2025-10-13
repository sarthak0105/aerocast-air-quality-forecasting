"use client"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const cities = ["Delhi", "Beijing", "Mexico City", "Cairo", "Lagos", "São Paulo"]

export default function CitySelector() {
  return (
    <div className="min-w-[180px]">
      <Select defaultValue="Delhi">
        <SelectTrigger aria-label="Select city">
          <SelectValue placeholder="Select city" />
        </SelectTrigger>
        <SelectContent>
          {cities.map((c) => (
            <SelectItem key={c} value={c}>
              {c}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}
