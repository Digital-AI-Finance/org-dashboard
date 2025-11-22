# Green-Finance

Academic course generation system for Green Finance Professional Certificate - 8-week course with learning-goal-driven pedagogy, Beamer slides, and interactive React app

[View on GitHub](https://github.com/Digital-AI-Finance/Green-Finance){ .md-button .md-button--primary }


---





## Information

| Property | Value |
|----------|-------|
| Language | TeX |
| Stars | 0 |
| Forks | 0 |
| Watchers | 0 |
| Open Issues | 0 |
| License | No License |
| Created | 2025-11-22 |
| Last Updated | 2025-11-22 |
| Last Push | 2025-11-22 |
| Contributors | 1 |
| Default Branch | main |
| Visibility | public |






## Datasets

This repository includes 8 dataset(s):

| Dataset | Format | Size |
|---------|--------|------|

| [settings.local.json](https://github.com/Digital-AI-Finance/Green-Finance/blob/main/.claude/settings.local.json) | .json | 0.16 KB |

| [package-lock.json](https://github.com/Digital-AI-Finance/Green-Finance/blob/main/react-app/package-lock.json) | .json | 692.86 KB |

| [package.json](https://github.com/Digital-AI-Finance/Green-Finance/blob/main/react-app/package.json) | .json | 1.4 KB |

| [data](https://github.com/Digital-AI-Finance/Green-Finance/blob/main/react-app/src/data) |  | 0.0 KB |

| [week1Slides.js](https://github.com/Digital-AI-Finance/Green-Finance/blob/main/react-app/src/data/week1Slides.js) | .js | 28.56 KB |

| [week1Slides_backup.js](https://github.com/Digital-AI-Finance/Green-Finance/blob/main/react-app/src/data/week1Slides_backup.js) | .js | 26.45 KB |

| [week1Slides_updated.js](https://github.com/Digital-AI-Finance/Green-Finance/blob/main/react-app/src/data/week1Slides_updated.js) | .js | 28.56 KB |

| [week1Slides_v3.js](https://github.com/Digital-AI-Finance/Green-Finance/blob/main/react-app/src/data/week1Slides_v3.js) | .js | 30.93 KB |




## Reproducibility


No specific reproducibility files found.







## Status





- Issues: Enabled
- Wiki: Disabled
- Pages: Enabled

## README

# Green Finance Professional Certificate

Academic course generation system for 8-week Green Finance course with learning-goal-driven pedagogy, Beamer LaTeX slides, and interactive React web application.

## Live Interactive App

**🌐 https://digital-ai-finance.github.io/Green-Finance**

Interactive Week 1 learning platform with 30 slides, charts, and self-assessment.

---

## Project Overview

### Course Structure
- **Duration:** 8 weeks
- **Format:** Academic professional certificate
- **Pedagogy:** Learning-goal-driven (3 goals per week)
- **Delivery:** Beamer PDF slides + Interactive web app

### Week 1 Status
✅ **Complete** - 37 slides, 17 charts, fully validated
- Core: 30 slides (3 learning goals × 10 slides)
- Supplementary: 7 empirical validation slides
- Interactive React app deployed

### Weeks 2-8 Status
⏳ **Ready for generation** using proven Week 1 template

---

## Quick Start

### View Interactive App
Visit: **https://digital-ai-finance.github.io/Green-Finance**

### Run Locally
```bash
cd react-app
npm install
npm start
# Opens at http://localhost:3000
```

### Compile LaTeX Slides
```bash
# Compile Week 1
pdflatex -interaction=nonstopmode 20251121_2306_Week1_v2_GreenFinanceFoundations.tex
pdflatex -interaction=nonstopmode 20251121_2306_Week1_v2_GreenFinanceFoundations.tex

# Clean up auxiliary files
Move-Item -Path *.aux,*.log,*.out,*.nav,*.toc,*.snm -Destination temp\ -ErrorAction SilentlyContinue
```

### Generate Charts
```powershell
# Generate all Week 1 charts
Get-ChildItem charts\week1\*.py | ForEach-Object { python $_.FullName }

# Generate Graphviz diagrams (requires Graphviz installed)
Get-ChildItem charts\week1\*.dot | ForEach-Object {
    dot -Tpdf $_.FullName -o ($_.FullName -replace '\.dot$','.pdf')
}
```

---

## Repository Structure

```
Green-Finance/
├── react-app/              # Interactive web app (Week 1)
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── charts/         # Interactive chart components
│   │   └── data/           # Course content (slides)
│   ├── DEPLOYMENT.md       # Deployment guide
│   └── package.json
│
├── charts/week1/           # Chart generation scripts
│   ├── week1_v2_goal1_*.py     # Goal 1 charts (matplotlib)
│   ├── week1_v2_goal2_*.py     # Goal 2 charts (matplotlib)
│   ├── week1_v2_goal3_*.py     # Goal 3 charts (matplotlib)
│   └── *.dot                    # Graphviz diagrams
│
├── agents/                 # Multi-agent system specs
│   ├── AGENT_3_ContentPlanner_v2.md
│   ├── AGENT_4_SlideGenerator_v2_LaTeXTemplates.md
│   └── README_v2.md
│
├── *.tex                   # LaTeX source files
├── *.pdf                   # Compiled slide PDFs
├── template_beamer_final.tex   # Madrid theme template
├── CLAUDE.md               # Project documentation
├── COURSE_GENERATOR_v2.md  # Generation system spec
└── DEPLOY_QUICKSTART.md    # Deployment quick start
```

---

## Features

### Interactive Web App
- ✅ 30 slides with keyboard navigation
- ✅ 3 learning goals with progress tracking
- ✅ Interactive charts (Recharts)
- ✅ Self-assessment quizzes
- ✅ LocalStorage persistence
- ✅ Mobile responsive
- ✅ GitHub Pages deployment

### LaTeX Slides (v2.0)
- ✅ Madrid theme (8pt, 16:9)
- ✅ 3 learning goals per week
- ✅ Goal-driven narrative structure
- ✅ 4 specialized slide types
- ✅ 17 charts (33%+ ratio)
- ✅ Bottom notes with goal tracking

### Multi-Agent System
- ✅ Course Orchestrator
- ✅ Guidelines Expert
- ✅ Content Planner v2.0
- ✅ Slide Generator v2.0
- ✅ YAML-based communication

---

## Technologies

### Web App
- React 18.2
- Material-UI 5.14
- Recharts 2.8 (charts)
- Framer Motion 10.16 (animations)
- D3 7.8 (advanced visualizations)

### Slides & Charts
- LaTeX Beamer (Madrid theme)
- Python 3.x + matplotlib
- Graphviz (diagrams)
- pdflatex

### Deployment
- GitHub Pages (automatic)
- GitHub Actions (CI/CD)

---

## Learning Goals (Week 1)

### Goal 1: Market Microstructure Theory
Understand the theoretical foundations explaining why green finance markets exist and how they function.

**Slides:** 1-10 | **Type:** Theoretical | **Charts:** Ecosystem diagrams

### Goal 2: Quantify Market Size & Growth
Quantify the size, growth trajectory, and composition of global green finance markets using empirical data.

**Slides:** 11-20 | **Type:** Quantitative | **Charts:** Time series, distributions

### Goal 3: Derive Pricing Models
Derive and apply mathematical models for pricing green financial instruments, incorporating greenium and ESG factors.

**Slides:** 21-30 | **Type:** Mathematical | **Charts:** Yield curves, risk-return

---

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Complete project documentation
- **[DEPLOY_QUICKSTART.md](DEPLOY_QUICKSTART.md)** - Deploy in 3 steps
- **[react-app/DEPLOYMENT.md](react-app/DEPLOYMENT.md)** - Full deployment guide
- **[COURSE_GENERATOR_v2.md](COURSE_GENERATOR_v2.md)** - System specification
- **[agents/README_v2.md](agents/README_v2.md)** - Multi-agent architecture

---

## Deployment

### Automatic (GitHub Actions)
1. Enable GitHub Pages: Settings → Pages → Source: **GitHub Actions**
2. Push changes: `git push origin main`
3. Visit: https://digital-ai-finance.github.io/Green-Finance

See **[DEPLOY_QUICKSTART.md](DEPLOY_QUICKSTART.md)** for detailed steps.

### Manual
```bash
cd react-app
npm run deploy
```

---

## Development Workflow

### Add New Week
1. Create content outline: `weekN_v2_content_outline.yaml`
2. Generate charts: `python charts/weekN/*.py`
3. Generate LaTeX: Use `AGENT_4_SlideGenerator_v2_LaTeXTemplates.md`
4. Compile: `pdflatex YYYYMMDD_HHMM_WeekN_Title.tex` (2x)
5. Validate: 30 slides, 10+ charts, 3 goals

### Update React App
1. Edit content: `react-app/src/data/week1Slides.js`
2. Test locally: `npm start`
3. Commit and push: Auto-deploys via GitHub Actions

---

## Quality Standards

### Per Week Requirements
- **Core slides:** 30 (3 goals × 10 slides)
- **Charts:** 10-11 minimum
- **Chart ratio:** ≥33%
- **Learning goals:** Exactly 3 (typed with narrative roles)
- **Statistics:** All verified via web search

### Color Scheme (Consistent)
- Primary (mlpurple): `#3333B2`
- Secondary (mllavender): `#ADADE0`
- Success (mlgreen): `#2CA02C`
- Warning (mlorange): `#FF7F0E`

---

## Prerequisites

- **Node.js** 18+ (for React app)
- **Python** 3.x (for charts)
- **pdflatex** (TeX Live or MiKTeX)
- **Graphviz** (for diagrams)
- **Git** (version control)

---

## Contributing

This is an academic project. For questions or improvements:
1. Open an issue
2. Submit a pull request
3. Contact: [Digital-AI-Finance organization](https://github.com/Digital-AI-Finance)

---

## License

Academic use. All rights reserved.

---

## Next Steps

- [ ] Generate Weeks 2-8
- [ ] Add more interactive features to web app
- [ ] Create student exercises
- [ ] Add video explanations
- [ ] Develop assessment module

---

**Version:** 2.0 (Learning-Goal-Driven)
**Status:** Week 1 Complete, Production Ready
**Live App:** https://digital-ai-finance.github.io/Green-Finance
