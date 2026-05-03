"use client"

import { HudWidget } from "./hud-widget"
import { MapPin, Globe } from "lucide-react"

export function NodeStatus() {
  return (
    <HudWidget title="Node Status">
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <MapPin className="w-4 h-4 text-purple-400" />
          <div>
            <p className="text-white text-sm font-medium">Vellore, IN</p>
            <p className="text-purple-400/60 text-[10px] uppercase tracking-wider">Primary Node</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <Globe className="w-4 h-4 text-purple-400" />
          <div>
            <div className="flex gap-4">
              <div>
                <p className="text-[10px] text-purple-400/60 uppercase tracking-wider">Lat</p>
                <p className="text-white text-xs font-mono">12.9716° N</p>
              </div>
              <div>
                <p className="text-[10px] text-purple-400/60 uppercase tracking-wider">Lng</p>
                <p className="text-white text-xs font-mono">79.1588° E</p>
              </div>
            </div>
          </div>
        </div>

        <div className="pt-2 border-t border-purple-500/20">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            <span className="text-[10px] text-green-400 uppercase tracking-wider">Online</span>
          </div>
        </div>
      </div>
    </HudWidget>
  )
}
