# llm-finance-portfolio

Research Portfolio: LLM in Financial Services

[View on GitHub](https://github.com/Digital-AI-Finance/llm-finance-portfolio){ .md-button .md-button--primary }


---





## Information

| Property | Value |
|----------|-------|
| Language | JavaScript |
| Stars | 0 |
| Forks | 0 |
| Watchers | 0 |
| Open Issues | 0 |
| License | No License |
| Created | 2025-12-06 |
| Last Updated | 2025-12-06 |
| Last Push | 2025-12-06 |
| Contributors | 1 |
| Default Branch | master |
| Visibility | public |






## Datasets

This repository includes 8 dataset(s):

| Dataset | Format | Size |
|---------|--------|------|

| [package-lock.json](https://github.com/Digital-AI-Finance/llm-finance-portfolio/blob/master/package-lock.json) | .json | 98.91 KB |

| [package.json](https://github.com/Digital-AI-Finance/llm-finance-portfolio/blob/master/package.json) | .json | 0.62 KB |

| [data](https://github.com/Digital-AI-Finance/llm-finance-portfolio/blob/master/src/data) |  | 0.0 KB |

| [course.json](https://github.com/Digital-AI-Finance/llm-finance-portfolio/blob/master/src/data/course.json) | .json | 9.36 KB |

| [notebooks.json](https://github.com/Digital-AI-Finance/llm-finance-portfolio/blob/master/src/data/notebooks.json) | .json | 3.6 KB |

| [publications.json](https://github.com/Digital-AI-Finance/llm-finance-portfolio/blob/master/src/data/publications.json) | .json | 3.96 KB |

| [researchAreas.json](https://github.com/Digital-AI-Finance/llm-finance-portfolio/blob/master/src/data/researchAreas.json) | .json | 4.26 KB |

| [siteConfig.json](https://github.com/Digital-AI-Finance/llm-finance-portfolio/blob/master/src/data/siteConfig.json) | .json | 1.93 KB |




## Reproducibility


No specific reproducibility files found.







## Status





- Issues: Enabled
- Wiki: Disabled
- Pages: Enabled

## README

# ING LLM Research Portfolio

This is the GitHub Pages website for the ING LLM research project, exploring Large Language Models in financial contexts.

## Development

### Prerequisites
- Node.js 18+ and npm

### Installation

```bash
npm install
```

### Development Server

```bash
npm run dev
```

The site will be available at `http://localhost:5173`

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Deployment

This site is configured for GitHub Pages deployment using HashRouter for client-side routing.

To deploy:

```bash
npm run deploy
```

This will build the site and push it to the `gh-pages` branch.

## Project Structure

```
github_page/
├── public/              # Static assets
├── src/
│   ├── components/      # Reusable React components
│   │   ├── Navbar.jsx
│   │   ├── Footer.jsx
│   │   ├── ThemeToggle.jsx
│   │   ├── ResearchCard.jsx
│   │   ├── PublicationCard.jsx
│   │   ├── NotebookCard.jsx
│   │   └── WeekTimeline.jsx
│   ├── pages/           # Page components
│   │   ├── Home.jsx
│   │   ├── Research.jsx
│   │   ├── Publications.jsx
│   │   ├── Notebooks.jsx
│   │   ├── Course.jsx
│   │   ├── About.jsx
│   │   └── Contact.jsx
│   ├── App.jsx          # Main app component with routing
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind CSS configuration
└── postcss.config.js    # PostCSS configuration
```

## Technology Stack

- **React 18** - UI framework
- **Vite** - Build tool
- **React Router** - Client-side routing (HashRouter for GitHub Pages)
- **Tailwind CSS** - Utility-first CSS framework
- **GitHub Pages** - Hosting

## Features

- Responsive design (mobile-first)
- Dark/light mode toggle with persistence
- Interactive research cards with expandable details
- Course timeline with weekly breakdown
- Notebook cards with Colab/Binder launch buttons
- SEO optimized
- Accessible navigation

## License

MIT License - see LICENSE file for details
