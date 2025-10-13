"use client"

import type React from "react"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Menu, Gauge, History, LineChartIcon, MapPinned, Settings, HelpCircle, Shield } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { useState } from "react"
import CitySelector from "./city-selector"

type AppShellProps = {
  children: React.ReactNode
}

const navItems = [
  { href: "/", label: "Dashboard", icon: Gauge },
  { href: "/historical", label: "Historical", icon: History },
  { href: "/analytics", label: "Analytics", icon: LineChartIcon },
  { href: "/locations", label: "Locations", icon: MapPinned },
  { href: "/settings", label: "Settings", icon: Settings },
  { href: "/about", label: "About", icon: HelpCircle },
  { href: "/admin", label: "Admin", icon: Shield },
]

export default function AppShell({ children }: AppShellProps) {
  const pathname = usePathname()
  const [open, setOpen] = useState(false)

  return (
    <div className="min-h-dvh bg-background text-foreground flex">
      {/* Sidebar */}
      <aside
        className={cn(
          "w-64 shrink-0 border-r border-border bg-[var(--sidebar,transparent)]/0 hidden md:flex md:flex-col",
        )}
        aria-label="Primary"
      >
        <div className="h-14 flex items-center px-4 border-b border-border">
          <Link href="/" className="font-medium">
            <span className="inline-flex items-center gap-2 text-balance">
              <span className="h-3 w-3 rounded-full" style={{ background: "var(--accent)" }} aria-hidden />
              Aero Cast
            </span>
          </Link>
        </div>
        <nav className="flex-1 p-2">
          <ul className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon
              const active = pathname === item.href
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    aria-current={active ? "page" : undefined}
                    className={cn(
                      "flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors",
                      active ? "bg-primary text-primary-foreground" : "hover:bg-secondary/10 text-foreground",
                    )}
                  >
                    <Icon className={cn("h-4 w-4", active ? "opacity-100" : "opacity-70")} aria-hidden />
                    <span>{item.label}</span>
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>
        <div className="p-4 text-xs text-muted-foreground">
          <p>NO₂ & O₃ insights</p>
        </div>
      </aside>

      {/* Mobile sidebar (overlay) */}
      {open && (
        <div className="fixed inset-0 z-40 md:hidden" role="dialog" aria-modal="true" aria-label="Mobile menu">
          <div className="absolute inset-0 bg-black/40" onClick={() => setOpen(false)} />
          <aside className="absolute left-0 top-0 h-full w-72 bg-background border-r border-border p-2">
            <div className="h-14 flex items-center px-2 border-b border-border">
              <span className="font-medium">Aero Cast</span>
            </div>
            <nav className="py-2">
              <ul className="space-y-1">
                {navItems.map((item) => {
                  const Icon = item.icon
                  const active = pathname === item.href
                  return (
                    <li key={item.href}>
                      <Link
                        href={item.href}
                        onClick={() => setOpen(false)}
                        className={cn(
                          "flex items-center gap-3 rounded-md px-3 py-2 text-sm",
                          active ? "bg-primary text-primary-foreground" : "hover:bg-secondary/10 text-foreground",
                        )}
                      >
                        <Icon className="h-4 w-4" aria-hidden />
                        <span>{item.label}</span>
                      </Link>
                    </li>
                  )
                })}
              </ul>
            </nav>
          </aside>
        </div>
      )}

      {/* Main column */}
      <div className="flex-1 flex flex-col">
        {/* Top bar */}
        <header className="h-14 border-b border-border bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="h-full container mx-auto max-w-7xl flex items-center gap-3 px-4">
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              aria-label="Open menu"
              onClick={() => setOpen(true)}
            >
              <Menu className="h-5 w-5" />
            </Button>
            <div className="flex-1 flex items-center gap-3">
              <CitySelector />
            </div>
            <div className="flex items-center gap-2">
              <span className="hidden sm:inline text-sm text-muted-foreground">Air Quality Platform</span>
            </div>
          </div>
        </header>

        <main className="container mx-auto max-w-7xl px-4 py-6">{children}</main>
      </div>
    </div>
  )
}
