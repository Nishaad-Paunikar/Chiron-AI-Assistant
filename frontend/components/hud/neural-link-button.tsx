"use client"

import { useState } from "react"
import { Zap, Loader2, CheckCircle2 } from "lucide-react"

export function NeuralLinkButton() {
  // Keeps track of what the button is doing
  const [status, setStatus] = useState<"idle" | "connecting" | "connected">("idle")

  const handleInitialize = async () => {
    // Prevent clicking it twice
    if (status !== "idle") return;

    setStatus("connecting")

    try {
      // 1. Sends the signal to your Python app.py
      const response = await fetch('http://localhost:8000/initialize', {
        method: 'POST',
      });

      if (response.ok) {
        // 2. Adds a slight delay so the UI feels like it's "booting up" a heavy AI model
        setTimeout(() => {
          setStatus("connected")
        }, 1500)
      } else {
        setStatus("idle")
        console.error("Failed to initialize.")
      }
    } catch (error) {
      console.error("Python Brain not responding:", error)
      setStatus("idle")
    }
  }

  return (
    <button
      onClick={handleInitialize}
      disabled={status !== "idle"}
      className={`
        relative group overflow-hidden rounded-full px-8 py-4 border transition-all duration-500
        ${status === 'idle' ? 'border-purple-500/50 bg-purple-900/20 hover:bg-purple-900/40 hover:border-purple-400 hover:shadow-[0_0_20px_rgba(168,85,247,0.4)] cursor-pointer' : ''}
        ${status === 'connecting' ? 'border-purple-400 bg-purple-900/40 shadow-[0_0_30px_rgba(168,85,247,0.6)] cursor-wait' : ''}
        ${status === 'connected' ? 'border-green-500/50 bg-green-900/20 shadow-[0_0_20px_rgba(34,197,94,0.4)] cursor-default' : ''}
      `}
    >
      <div className="flex items-center gap-3">
        {/* Swaps the icon based on the current status */}
        {status === 'idle' && <Zap className="w-5 h-5 text-purple-400" />}
        {status === 'connecting' && <Loader2 className="w-5 h-5 text-purple-400 animate-spin" />}
        {status === 'connected' && <CheckCircle2 className="w-5 h-5 text-green-400" />}

        {/* Swaps the text based on the current status */}
        <span className={`font-mono uppercase tracking-[0.2em] text-sm ${status === 'connected' ? 'text-green-400' : 'text-white'}`}>
          {status === 'idle' && "Initialize Neural Link"}
          {status === 'connecting' && "Establishing Link..."}
          {status === 'connected' && "Link Established"}
        </span>
      </div>
    </button>
  )
}