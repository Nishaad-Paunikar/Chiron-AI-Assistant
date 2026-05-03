"use client"

export function CentralOrb() {
  return (
    <div className="flex flex-col items-center justify-center gap-8">
      {/* Outer Ring */}
      <div className="relative">
        {/* Decorative rings */}
        <div className="absolute inset-0 w-64 h-64 md:w-80 md:h-80 rounded-full border border-purple-500/20 animate-[spin_20s_linear_infinite]" />
        <div className="absolute inset-4 w-56 h-56 md:w-72 md:h-72 rounded-full border border-purple-500/30 animate-[spin_15s_linear_infinite_reverse]" />
        
        {/* Main Orb */}
        <div className="w-64 h-64 md:w-80 md:h-80 rounded-full flex items-center justify-center">
          <div 
            className="w-40 h-40 md:w-52 md:h-52 rounded-full orb-pulse"
            style={{
              background: 'radial-gradient(circle at 30% 30%, rgba(192, 132, 252, 0.8), rgba(168, 85, 247, 0.6), rgba(126, 34, 206, 0.4), rgba(88, 28, 135, 0.2))',
            }}
          >
            <div 
              className="w-full h-full rounded-full flex items-center justify-center"
              style={{
                background: 'radial-gradient(circle at 40% 40%, rgba(255, 255, 255, 0.2), transparent 60%)',
              }}
            >
              {/* Inner core highlight */}
              <div 
                className="w-8 h-8 md:w-12 md:h-12 rounded-full"
                style={{
                  background: 'radial-gradient(circle, rgba(255, 255, 255, 0.4), transparent)',
                  filter: 'blur(4px)',
                }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* CHIRON Text */}
      <div className="text-center">
        <h1 
          className="text-4xl md:text-6xl font-bold tracking-[0.5em] text-white"
          style={{ 
            fontFamily: 'var(--font-orbitron), sans-serif',
            textShadow: '0 0 20px rgba(168, 85, 247, 0.8), 0 0 40px rgba(168, 85, 247, 0.4)',
          }}
        >
          CHIRON
        </h1>
        <p className="text-purple-400/60 text-xs tracking-[0.4em] mt-2 uppercase">
          Neural Interface v2.4.1
        </p>
      </div>
    </div>
  )
}
