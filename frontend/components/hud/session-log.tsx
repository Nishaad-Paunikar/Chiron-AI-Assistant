"use client"

import { useState, useEffect } from "react"
import { HudWidget } from "./hud-widget"
import { User, Shield, Clock } from "lucide-react"

export function SessionLog() {
  // 1. Create a variable to hold the live time
  const [sessionTime, setSessionTime] = useState("00:00:00")

  // 2. This is the engine for the stopwatch
  useEffect(() => {
    // Record the exact millisecond the HUD finishes loading
    const startTime = Date.now()

    const updateTimer = () => {
      const now = Date.now()
      // Calculate how many total seconds have passed
      const diffInSeconds = Math.floor((now - startTime) / 1000)

      // Break that down into hours, minutes, and seconds
      const hours = Math.floor(diffInSeconds / 3600)
      const minutes = Math.floor((diffInSeconds % 3600) / 60)
      const seconds = diffInSeconds % 60

      // Format it so it always has two digits (e.g., "05" instead of just "5")
      const formattedTime =
        String(hours).padStart(2, '0') + ':' +
        String(minutes).padStart(2, '0') + ':' +
        String(seconds).padStart(2, '0')

      // Update the screen with the new time
      setSessionTime(formattedTime)
    }

    // Tell the component to run that math every 1 second
    const interval = setInterval(updateTimer, 1000)

    // Clean up the timer if we navigate away
    return () => clearInterval(interval)
  }, [])

  return (
    <HudWidget title="Session Log">
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full border border-purple-500/50 flex items-center justify-center bg-purple-500/10">
            <User className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <p className="text-white text-sm font-medium">Nishaad Paunikar</p>
            <p className="text-purple-400/60 text-[10px] uppercase tracking-wider">Administrator</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Shield className="w-3 h-3 text-green-400" />
          <span className="text-[10px] text-green-400 uppercase tracking-wider">Authenticated</span>
        </div>

        <div className="pt-2 border-t border-purple-500/20 space-y-2">
          <div className="flex items-center gap-2">
            <Clock className="w-3 h-3 text-purple-400/60" />
            <span className="text-[10px] text-purple-400/60 uppercase tracking-wider">Session Duration</span>
          </div>
          {/* 3. The hardcoded time is gone, replaced by our live variable */}
          <p className="text-white text-xs font-mono pl-5">{sessionTime}</p>
        </div>
      </div>
    </HudWidget>
  )
}