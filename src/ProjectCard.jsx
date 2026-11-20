function ProjectCard({ title, description, link, tags = [] }) {
  return (
    <div className="project-card">
      <h3>{title}</h3>
      <p>{description}</p>
      {tags.length > 0 && (
        <ul className="tags" aria-label="Technologies used">
          {tags.map((tag) => (
            <li key={tag}>{tag}</li>
          ))}
        </ul>
      )}
      <a href={link} target="_blank" rel="noopener noreferrer">View Project →</a>
    </div>
  )
}

export default ProjectCard