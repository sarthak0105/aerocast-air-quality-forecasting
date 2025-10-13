import type React from "react"
import AppShell from "@/components/aero/app-shell"

export default function AeroLayout({ children }: { children: React.ReactNode }) {
  return <AppShell>{children}</AppShell>
}
