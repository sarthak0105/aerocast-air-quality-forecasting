'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'

export function Footer() {
  const footerLinks = [
    { href: '/health', label: 'System Health', icon: 'fas fa-heart-pulse' },
    { href: '#', label: 'Download Data', icon: 'fas fa-download' },
    { href: '#', label: 'Contact', icon: 'fas fa-envelope' },
    { href: '/docs', label: 'API Documentation', icon: 'fas fa-book' },
  ]

  return (
    <footer className="bg-gradient-to-r from-gray-700 to-gray-800 text-white">
      <div className="p-6 text-center">
        <motion.p 
          className="text-lg mb-4 opacity-90"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          Powered by AI/ML models using satellite data and meteorological analysis
        </motion.p>
        
        <motion.div 
          className="flex flex-wrap justify-center gap-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          {footerLinks.map((link, index) => (
            <motion.div
              key={link.href}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Link
                href={link.href}
                className="flex items-center gap-2 text-white/80 hover:text-white transition-colors duration-300 px-3 py-2 rounded-lg hover:bg-white/10"
              >
                <i className={link.icon}></i>
                <span>{link.label}</span>
              </Link>
            </motion.div>
          ))}
        </motion.div>

        <div className="mt-6 pt-4 border-t border-white/20">
          <p className="text-sm text-white/60">
            © 2024 AeroCast - Advanced Air Quality Forecasting Platform
          </p>
        </div>
      </div>
    </footer>
  )
}