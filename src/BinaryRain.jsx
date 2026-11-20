import { useEffect, useRef } from 'react'

// Subtle falling 1s and 0s behind the page.
// Tweak these to taste:
const FONT_SIZE = 16        // size of each digit, in pixels
const COLUMN_GAP = 3.2      // higher = fewer columns (sparser rain)
const SPEED = 0.35          // how many rows a column falls per frame step (lower = slower)
const STEP_MS = 50          // time between frame steps
const OPACITY = 0.16        // overall strength of the effect (0 to 1)

function BinaryRain() {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')

    // Respect visitors who turned off animations on their device
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    let width, height, columns, drops
    let animationId
    let lastStep = 0

    function setup() {
      const dpr = window.devicePixelRatio || 1
      width = window.innerWidth
      height = window.innerHeight
      canvas.width = width * dpr
      canvas.height = height * dpr
      canvas.style.width = width + 'px'
      canvas.style.height = height + 'px'
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      ctx.font = `${FONT_SIZE}px 'JetBrains Mono', monospace`

      const spacing = FONT_SIZE * COLUMN_GAP
      const count = Math.ceil(width / spacing)
      columns = Array.from({ length: count }, (_, i) => i * spacing)
      // start each column at a random spot on screen so rain is visible right away
      drops = columns.map(() => ({
        y: Math.random() * height / FONT_SIZE,
        speed: SPEED * (0.6 + Math.random() * 0.8),
      }))
    }

    function draw() {
      // fade the previous frame slightly, leaving short trails
      ctx.fillStyle = 'rgba(10, 14, 10, 0.12)'
      ctx.fillRect(0, 0, width, height)

      drops.forEach((drop, i) => {
        const prevRow = Math.floor(drop.y)
        drop.y += drop.speed
        const row = Math.floor(drop.y)
        const y = row * FONT_SIZE

        // only draw a new digit when the column reaches a new row,
        // so digits sit cleanly one under another instead of smudging
        if (row !== prevRow) {
          const digit = Math.random() > 0.5 ? '1' : '0'
          ctx.fillStyle = '#33ff33'
          ctx.fillText(digit, columns[i], y)
        }
        // once a column passes the bottom, restart it at the top after a random pause
        if (y > height && Math.random() > 0.975) {
          drop.y = Math.random() * -20
          drop.speed = SPEED * (0.6 + Math.random() * 0.8)
        }
      })
    }

    function loop(time) {
      if (time - lastStep >= STEP_MS) {
        draw()
        lastStep = time
      }
      animationId = requestAnimationFrame(loop)
    }

    setup()
    if (reduceMotion) {
      // draw a few still frames instead of animating
      for (let i = 0; i < 200; i++) draw()
    } else {
      animationId = requestAnimationFrame(loop)
    }

    // pause when the tab is hidden, to save battery
    function onVisibility() {
      if (reduceMotion) return
      if (document.hidden) cancelAnimationFrame(animationId)
      else animationId = requestAnimationFrame(loop)
    }

    window.addEventListener('resize', setup)
    document.addEventListener('visibilitychange', onVisibility)
    return () => {
      cancelAnimationFrame(animationId)
      window.removeEventListener('resize', setup)
      document.removeEventListener('visibilitychange', onVisibility)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="binary-rain"
      style={{ opacity: OPACITY }}
      aria-hidden="true"
    />
  )
}

export default BinaryRain