"use client"

import { HudWidget } from "./hud-widget"
import { Terminal } from "lucide-react"

const logs = [
  { time: "14:32:01", msg: "[SYS] Neural link initialized" },
  { time: "14:32:03", msg: "[GPU] CUDA cores activated" },
  { time: "14:32:05", msg: "[NET] Establishing secure tunnel" },
  { time: "14:32:07", msg: "[AUTH] Biometric scan complete" },
  { time: "14:32:09", msg: "[SYS] Loading model weights..." },
  { time: "14:32:12", msg: "[AI] Transformer loaded" },
  { time: "14:32:14", msg: "[SYS] Memory allocation: 4.2GB" },
  { time: "14:32:16", msg: "[NET] Latency: 23ms" },
  { time: "14:32:18", msg: "[SYS] All systems operational" },
  { time: "14:32:20", msg: "[AI] Ready for input" },
]

export function ActivityMonitor() {
  return (
    <HudWidget title="Activity Monitor">
      <div className="space-y-2">
        <div className="flex items-center gap-2 pb-2 border-b border-purple-500/20">
          <Terminal className="w-3 h-3 text-purple-400" />
          <span className="text-[10px] text-purple-400/80 uppercase tracking-wider">Terminal Output</span>
        </div>
        
        <div className="h-32 overflow-hidden relative">
          <div className="terminal-scroll space-y-1">
            {[...logs, ...logs].map((log, i) => (
              <div key={i} className="flex gap-2 text-[10px] font-mono">
                <span className="text-purple-500/60">{log.time}</span>
                <span className="text-purple-300/80">{log.msg}</span>
              </div>
            ))}
          </div>
          <div className="absolute bottom-0 left-0 right-0 h-8 bg-gradient-to-t from-black/80 to-transparent pointer-events-none" />
        </div>
      </div>
    </HudWidget>
  )
}
