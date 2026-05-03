"use client"

import { useState, useEffect } from "react"
import { CentralOrb } from "@/components/hud/central-orb"
import { NodeStatus } from "@/components/hud/node-status"
import { SystemVitals } from "@/components/hud/system-vitals"
import { ActivityMonitor } from "@/components/hud/activity-monitor"
import { SessionLog } from "@/components/hud/session-log"
import { NeuralLinkButton } from "@/components/hud/neural-link-button"

export default function ChironHUD() {
  const [cpuUsage, setCpuUsage] = useState(0)
  const [memoryUsage, setMemoryUsage] = useState("0.0 GB")
  const [gpuUsage, setGpuUsage] = useState(0)
  const [temp, setTemp] = useState(0)

  useEffect(() => {
    const fetchVitals = async () => {
      try {
        const response = await fetch('http://localhost:8000/system-vitals')
        const data = await response.json()

        setCpuUsage(data.cpu_usage || 0)
        setGpuUsage(data.gpu_usage || 0)
        setTemp(data.temp || 0)
        setMemoryUsage(data.ram_usage_gb ? `${data.ram_usage_gb} GB` : "0.0 GB")
      } catch (error) {
        console.error("Connection to Chiron Brain failed:", error)
      }
    }

    const interval = setInterval(fetchVitals, 2000)
    return () => clearInterval(interval)
  }, [])

  return (
    <main className="min-h-screen w-full bg-black relative overflow-hidden">
      <div className="absolute inset-0 hex-background" />
      <div className="absolute inset-0 scanline pointer-events-none" />
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: 'radial-gradient(ellipse at center, transparent 0%, rgba(0,0,0,0.6) 100%)',
        }}
      />

      <div className="relative z-10 min-h-screen flex flex-col p-4 md:p-8">
        <div className="flex justify-between items-start mb-8">
          <div className="text-[10px] text-purple-400/60 font-mono uppercase tracking-wider">
            <span>System Status: </span>
            <span className="text-green-400">Operational</span>
          </div>
          <div className="text-[10px] text-purple-400/60 font-mono uppercase tracking-wider">
            {new Date().toLocaleDateString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric'
            })}
          </div>
        </div>

        <div className="flex-1 grid grid-cols-1 lg:grid-cols-[280px_1fr_280px] gap-6 items-center">
          <div className="flex flex-col gap-6 order-2 lg:order-1">
            <NodeStatus />
            <SystemVitals
              cpuUsage={cpuUsage}
              memoryUsage={memoryUsage}
              gpuUsage={gpuUsage}
              temp={temp}
            />
          </div>

          <div className="flex items-center justify-center order-1 lg:order-2 py-8 lg:py-0">
            <CentralOrb />
          </div>

          <div className="flex flex-col gap-6 order-3">
            <ActivityMonitor />
            <SessionLog />
          </div>
        </div>

        <div className="flex justify-center pt-8 pb-4">
          <NeuralLinkButton />
        </div>

        <div className="flex justify-between items-center text-[9px] text-purple-400/40 font-mono uppercase tracking-wider">
          <span>CHIRON AI v2.4.1</span>
          <span>Quantum Secure Connection</span>
          <span>Node: Primary</span>
        </div>
      </div>
    </main>
  )
}