"use client"

import { cn } from "@/lib/utils"
import { ReactNode } from "react"

interface HudWidgetProps {
  title: string
  children: ReactNode
  className?: string
}

export function HudWidget({ title, children, className }: HudWidgetProps) {
  return (
    <div
      className={cn(
        "relative border border-purple-500/30 bg-purple-500/5 backdrop-blur-md rounded-sm p-4",
        "widget-glow corner-tr corner-bl",
        className
      )}
    >
      <div className="absolute -top-3 left-4 px-2 bg-black">
        <span className="text-[10px] uppercase tracking-[0.3em] text-purple-400 font-medium">
          {title}
        </span>
      </div>
      <div className="pt-2">
        {children}
      </div>
    </div>
  )
}
