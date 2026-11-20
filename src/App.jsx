import { useState, useEffect } from 'react'
import './App.css'
import ProjectCard from './ProjectCard'
import BinaryRain from './BinaryRain'

const projects = [
  {
    title: "Forecasting or Estimating? Irradiance Leakage in Solar Forecasting",
    description: "Submitted to AAAI (time series analysis track). A revised and extended version of my master's thesis, with reproducible code. The paper shows how using target-hour irradiance quietly turns 'forecasting' into 'estimating' in hourly solar power prediction. Uses six years of one-minute data from a 10 MW solar plant plus NASA POWER weather data to compare linear regression, XGBoost, LSTM and MLP models, with and without the leaked feature, at 1–24 hour horizons. Results are backed by Diebold–Mariano significance tests and data checks for clock alignment, sensor gaps, temperature and snow.",
    link: "https://github.com/IsaacTsolak/pv-forecasting-or-estimating",
    tags: ["Python", "PyTorch", "XGBoost", "scikit-learn", "pandas", "Time Series"]
  },
  {
    title: "Solar Power Forecasting with AI",
    description: "My master's thesis at Wentworth Institute of Technology, applying ML models (XGBoost, LSTM, Random Forest, and more) to forecast solar power generation from historical output and NASA weather data. XGBoost achieved a 71.2% error reduction over baseline, with an R² of 0.987. This work became the foundation for my AAAI submission, Forecasting or Estimating?",
    link: "https://github.com/IsaacTsolak/solar-forecasting-thesis",
    tags: ["Python", "TensorFlow / Keras", "XGBoost", "scikit-learn", "pandas", "Time Series"]
  },
  {
    title: "Job Application Tracker Agent",
    description: "A personal agent that reads my Gmail through the Gmail API, picks out job-application emails, and tracks where each application stands. A rule-based classifier tags confirmations, rejections and interview invites and pulls out company names. Anything it isn't sure about gets flagged for review instead of guessed. Results go into a duplicate-safe SQLite store, and every component has its own tests.",
    link: "https://github.com/IsaacTsolak/app-tracker",
    tags: ["Python", "Gmail API", "OAuth", "SQLite", "Unit Testing"]
  },
  {
    title: "NLP Question Generator",
    description: "An end-to-end system that turns educational text into complete multiple-choice questions with plausible distractors, combining pre-trained question generation, entity extraction, and semantic similarity — built for student practice problems and educator time-saving.",
    link: "https://github.com/IsaacTsolak/NLP_Question_Generator",
    tags: ["Python", "Hugging Face Transformers", "spaCy", "Sentence-Transformers", "Gradio", "NLP"]
  },
  {
    title: "High-Value Purchase Prediction",
    description: "Predicts whether an online retail transaction is high-value using only pre-sale signals — timing, quantity, and country — deliberately excluding price. Compares Logistic Regression, Random Forest, and a voting ensemble to see whether combining models improves accuracy.",
    link: "https://github.com/IsaacTsolak/Transaction_value_predictor",
    tags: ["Python", "scikit-learn", "pandas", "Ensemble Models", "Classification"]
  },
  {
    title: "Stock Market Regime Clustering",
    description: "Applies K-Means clustering and PCA to identify distinct market 'regimes' in historical AAPL and NVDA stock data (2019–2025), using engineered features — returns, rolling volatility, and moving averages — to group trading days into behavioral clusters like stable, bullish, and high-volatility periods.",
    link: "https://github.com/IsaacTsolak/stock_market_clustering.git",
    tags: ["Python", "scikit-learn", "K-Means", "PCA", "yfinance"]
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
    <>
    <BinaryRain />
    <div className="page">
      <header>
        <h1>Isaac Tsolak</h1>
        <p>AI Engineer</p>
        <nav className="header-links">
          <a href="https://github.com/IsaacTsolak" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="https://www.linkedin.com/in/isaactsolak" target="_blank" rel="noopener noreferrer">LinkedIn</a>
          <a href="mailto:isaac.tsolak@gmail.com">Email</a>
          <a className="resume-button" href="/resume.pdf" target="_blank" rel="noopener noreferrer">Résumé ↓</a>
        </nav>
      </header>

      <section>
        <h2>About</h2>
        <p className="lead">
          I build machine learning systems end to end, from feature engineering and model
          selection to the interfaces people actually use.
        </p>
        <p>
          My work spans time-series forecasting (including a paper submitted to AAAI on solar
          power prediction), NLP, and unsupervised learning, using Python, scikit-learn, and React.
          I hold an MS in Applied Computer Science from Wentworth Institute of Technology
          and a BA in Psychology from Boston University.
        </p>
        <p>
          Alongside my studies, I spent half a decade in client-facing roles, most recently as
          Head Bartender. That combination shapes how I build: technically rigorous, but always
          with the end user in mind.
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
            tags={project.tags}
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
    </>
  )
}

export default App