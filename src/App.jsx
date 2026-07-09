import { useState, useEffect } from 'react'
import './App.css'
import ProjectCard from './ProjectCard'

const projects = [
  {
    title: "Solar Power Forecasting with AI",
    description: "Thesis research applying ML models (XGBoost, LSTM, Random Forest, and more) to forecast solar power generation from historical output and NASA weather data. XGBoost achieved a 71.2% error reduction over baseline, with an R² of 0.987 — pending publication at the North American Power Symposium 2026.",
    link: "https://github.com/IsaacTsolak/solar-forecasting-thesis"
  },
  {
    title: "NLP Question Generator",
    description: "An end-to-end system that turns educational text into complete multiple-choice questions with plausible distractors, combining pre-trained question generation, entity extraction, and semantic similarity — built for student practice problems and educator time-saving.",
    link: "https://github.com/IsaacTsolak/NLP_Question_Generator"
  },
  {
    title: "High-Value Purchase Prediction",
    description: "Predicts whether an online retail transaction is high-value using only pre-sale signals — timing, quantity, and country — deliberately excluding price. Compares Logistic Regression, Random Forest, and a voting ensemble to see whether combining models improves accuracy.",
    link: "https://github.com/IsaacTsolak/Transaction_value_predictor"
  },
  {
    title: "Stock Market Regime Clustering",
    description: "Applies K-Means clustering and PCA to identify distinct market 'regimes' in historical AAPL and NVDA stock data (2019–2025), using engineered features — returns, rolling volatility, and moving averages — to group trading days into behavioral clusters like stable, bullish, and high-volatility periods.",
    link: "https://github.com/IsaacTsolak/stock_market_clustering.git"
  }
]

function BootSequence({ onComplete }) {
  const [lines, setLines] = useState([])

  const bootLines = [
    "Initializing system...",
    "Loading profile: Isaac...",
    "Mounting portfolio.exe...",
    "Connection established.",
    "Welcome."
  ]

  useEffect(() => {
    bootLines.forEach((line, i) => {
      setTimeout(() => {
        setLines(prev => [...prev, line])
      }, i * 400)
    })

    setTimeout(() => {
      onComplete()
    }, bootLines.length * 400 + 500)
  }, [])

  return (
    <div className="boot-screen">
      {lines.map((line, i) => (
        <p key={i}>{line}</p>
      ))}
    </div>
  )
}

function App() {
  const [booted, setBooted] = useState(false)

  if (!booted) {
    return <BootSequence onComplete={() => setBooted(true)} />
  }

  return (
    <div>
      <header>
        <h1>Isaac</h1>
        <p>ML Engineer & builder</p>
      </header>

      <section>
        <h2>About</h2>
        <p>
        I build machine learning systems end-to-end from feature engineering and model 
        selection to the interfaces people actually use. My work spans time-series forecasting 
        (potential publication on solar energy prediction), NLP, and unsupervised learning, using Python, 
        scikit-learn, and React. Before and during my MS in Applied Computer Science, I spent a decade in 
        client-facing roles, most recently as Head Bartender and previouly earned a psychology degree from Boston University 
        along the way. That combination shapes how I build: technically rigorous, but always with the end user in mind.
        </p>
      </section>

      <section>
        <h2>Projects</h2>
        {projects.map((project, index) => (
          <ProjectCard
            key={index}
            title={project.title}
            description={project.description}
            link={project.link}
          />
        ))}
      </section>

      <section>
        <h2>Contact</h2>
        <p>
          <a href="mailto:isaac.tsolak@gmail.com">isaac.tsolak@gmail.com</a>
        </p>
        <p>
          <a href="https://www.linkedin.com/in/isaactsolak" target="_blank" rel="noopener noreferrer">LinkedIn</a>
        </p>
        <p>
          <a href="https://github.com/IsaacTsolak" target="_blank" rel="noopener noreferrer">GitHub</a>
        </p>
      </section>
    </div>
  )
}

export default App