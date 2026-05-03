"use client"

import { HudWidget } from "./hud-widget"
import { Cpu, MonitorDot } from "lucide-react"

interface VitalBarProps {
  label: string
  value: number
  icon: React.ReactNode
}

function VitalBar({ label, value, icon }: VitalBarProps) {
  const safeValue = Math.round(value || 0)

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          {icon}
          <span className="text-[10px] text-purple-400/80 uppercase tracking-wider">{label}</span>
        </div>
        <span className="text-xs font-mono text-white">{safeValue}%</span>
      </div>
      <div className="h-2 bg-purple-900/30 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full progress-bar transition-all duration-500"
          style={{
            width: `${safeValue}%`,
            background: 'linear-gradient(90deg, rgba(168, 85, 247, 0.6), rgba(168, 85, 247, 1))',
            boxShadow: '0 0 10px rgba(168, 85, 247, 0.8)',
          }}
        />
      </div>
    </div>
  )
}

interface SystemVitalsProps {
  cpuUsage?: number;
  memoryUsage?: string;
  gpuUsage?: number;
  temp?: number;
}

export function SystemVitals({ cpuUsage = 0, memoryUsage = "0.0 GB", gpuUsage = 0, temp = 0 }: SystemVitalsProps) {
  return (
    <HudWidget title="System Vitals">
      <div className="space-y-4">
        <VitalBar
          label="RTX 3050 GPU"
          value={gpuUsage}
          icon={<MonitorDot className="w-3 h-3 text-purple-400" />}
        />

        <VitalBar
          label="CPU Usage"
          value={cpuUsage}
          icon={<Cpu className="w-3 h-3 text-purple-400" />}
        />

        <div className="pt-2 border-t border-purple-500/20 grid grid-cols-2 gap-2">
          <div>
            <p className="text-[10px] text-purple-400/60 uppercase tracking-wider">Temp</p>
            <p className="text-white text-xs font-mono">{temp}°C</p>
          </div>
          <div>
            <p className="text-[10px] text-purple-400/60 uppercase tracking-wider">Memory</p>
            <p className="text-white text-xs font-mono">{memoryUsage}</p>
          </div>
        </div>
      </div>
    </HudWidget>
  )
}