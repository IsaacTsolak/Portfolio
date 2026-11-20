import { useEffect, useState } from 'react'
import logLines from './logLines'

// Faint terminal log that scrolls in the background, built from real results.
// Tweak these to taste:
const VISIBLE_LINES = 60     // how many lines stay on screen
const TYPE_SPEED_MS = 8     // time per character while a line types out
const LINE_PAUSE_MS = 250    // pause after a line finishes, before the next one

function TrainingLog() {
  const reduceMotion =
    typeof window !== 'undefined' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches

  // finished lines, plus the line currently being typed
  const [done, setDone] = useState(() =>
    reduceMotion ? logLines.slice(0, VISIBLE_LINES) : logLines.slice(0, 12)
  )
  const [index, setIndex] = useState(reduceMotion ? 0 : 12)
  const [typed, setTyped] = useState('')
  const [visible, setVisible] = useState(true)

  // pause while the tab isn't visible, to save battery
  useEffect(() => {
    const onChange = () => setVisible(!document.hidden)
    document.addEventListener('visibilitychange', onChange)
    return () => document.removeEventListener('visibilitychange', onChange)
  }, [])

  useEffect(() => {
    if (reduceMotion || !visible) return

    const line = logLines[index % logLines.length]
    let timer

    if (typed.length < line.length) {
      // type the next character
      timer = setTimeout(() => setTyped(line.slice(0, typed.length + 1)), TYPE_SPEED_MS)
    } else {
      // line finished: move it into the log and start the next one
      timer = setTimeout(() => {
        setDone((prev) => [...prev, line].slice(-VISIBLE_LINES))
        setTyped('')
        setIndex((i) => i + 1)
      }, LINE_PAUSE_MS)
    }

    return () => clearTimeout(timer)
  }, [typed, index, visible, reduceMotion])

  return (
    <div className="training-log" aria-hidden="true">
      <div className="training-log-inner">
        {done.map((line, i) => (
          <div key={i}>{line}</div>
        ))}
        {!reduceMotion && (
          <div className="training-log-current">
            {typed}
            <span className="training-log-cursor">▊</span>
          </div>
        )}
      </div>
    </div>
  )
}

export default TrainingLog