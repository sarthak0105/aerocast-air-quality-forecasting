'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion } from 'framer-motion'

interface HeaderProps {
  currentPage?: string
}

export function Header({ currentPage }: HeaderProps) {
  const pathname = usePathname()
  
  const navItems = [
    { href: '/', label: 'Dashboard', icon: 'fas fa-home' },
    { href: '/historical', label: 'Historical', icon: 'fas fa-chart-line' },
    { href: '/analytics', label: 'Analytics', icon: 'fas fa-chart-bar' },
    { href: '/settings', label: 'Settings', icon: 'fas fa-cog' },
  ]

  const isActive = (href: string) => {
    if (href === '/') return pathname === '/'
    return pathname.startsWith(href)
  }

  return (
    <div className="gradient-primary text-white relative overflow-hidden">
      {/* Floating orbs background */}
      <div className="absolute inset-0 floating-orbs pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-white/10 rounded-full blur-2xl" />
        <div className="absolute bottom-1/4 right-1/4 w-24 h-24 bg-white/15 rounded-full blur-xl" />
      </div>

      {/* Header content */}
      <div className="relative z-10 text-center py-12 px-8">
        <motion.h1 
          className="text-4xl md:text-5xl font-bold mb-4 text-shadow-lg"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <i className="fas fa-wind mr-4 gentle-float"></i>
          AeroCast
        </motion.h1>
        
        <motion.p 
          className="text-lg md:text-xl opacity-90"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          AI-powered air quality forecasting for Delhi NCR region
        </motion.p>
      </div>

      {/* Navigation */}
      <div className="bg-white/10 backdrop-blur-sm py-4">
        <div className="flex justify-center">
          <nav className="flex flex-wrap gap-2 md:gap-8">
            {navItems.map((item, index) => (
              <motion.div
                key={item.href}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
              >
                <Link
                  href={item.href}
                  className={`
                    flex items-center gap-2 px-4 py-2 rounded-full font-medium transition-all duration-300
                    ${isActive(item.href) 
                      ? 'bg-white/20 text-white shadow-lg transform scale-105' 
                      : 'text-white/80 hover:bg-white/10 hover:text-white hover:transform hover:scale-105'
                    }
                  `}
                >
                  <i className={item.icon}></i>
                  <span className="hidden sm:inline">{item.label}</span>
                </Link>
              </motion.div>
            ))}
          </nav>
        </div>
      </div>

      {/* Bottom gradient line */}
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/30 to-transparent" />
    </div>
  )
}