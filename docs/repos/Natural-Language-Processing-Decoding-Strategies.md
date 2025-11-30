# Natural-Language-Processing-Decoding-Strategies



[View on GitHub](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies){ .md-button .md-button--primary }


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
| Created | 2025-11-30 |
| Last Updated | 2025-11-30 |
| Last Push | 2025-11-30 |
| Contributors | 1 |
| Default Branch | main |
| Visibility | private |




## Notebooks

This repository contains 2 notebook(s):

| Notebook | Language | Type |
|----------|----------|------|

| [week09_decoding_lab](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies/blob/main/lab/week09_decoding_lab.ipynb) | PYTHON | jupyter |

| [week09_decoding_simplified](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies/blob/main/lab/week09_decoding_simplified.ipynb) | PYTHON | jupyter |




## Datasets

This repository includes 10 dataset(s):

| Dataset | Format | Size |
|---------|--------|------|

| [package.json](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies/blob/main/learning-app/package.json) | .json | 0.9 KB |

| [data](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies/blob/main/learning-app/src/data) |  | 0.0 KB |

| [learningGoals.js](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies/blob/main/learning-app/src/data/learningGoals.js) | .js | 3.15 KB |

| [week09_slides_complete.json](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies/blob/main/learning-app/src/week09_slides_complete.json) | .json | 97.94 KB |

| [package.json](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies/blob/main/react-app/package.json) | .json | 0.95 KB |

| [data](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies/blob/main/react-app/src/data) |  | 0.0 KB |

| [extractedSlides.json](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies/blob/main/react-app/src/data/extractedSlides.json) | .json | 65.19 KB |

| [quantitativeExamples.js](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies/blob/main/react-app/src/data/quantitativeExamples.js) | .js | 6.84 KB |

| [slideContent.js](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies/blob/main/react-app/src/data/slideContent.js) | .js | 7.72 KB |

| [week09_slides_complete.json](https://github.com/Digital-AI-Finance/Natural-Language-Processing-Decoding-Strategies/blob/main/react-app/src/data/week09_slides_complete.json) | .json | 97.94 KB |




## Reproducibility


No specific reproducibility files found.







## Status





- Issues: Enabled
- Wiki: Disabled
- Pages: Disabled

## README

# Natural Language Processing: Decoding Strategies

**Week 9 Module** - Interactive learning platform for understanding text generation decoding methods in Large Language Models.

## Overview

This repository contains a complete educational module on decoding strategies, featuring:
- **2 Interactive React Applications** for hands-on learning
- **Comprehensive Teaching Materials** (slides, notebooks, charts)
- **6 Decoding Algorithm Implementations** (greedy, beam, temperature, top-k, nucleus, contrastive)
- **67 Professional Visualizations** (Python-generated PDF charts)

## Quick Start

### Learning App (Structured Course)
```bash
cd learning-app
npm install
npm run dev
# Open http://localhost:5180
```

### Interactive Playground (Experimentation)
```bash
cd react-app
npm install
npm run dev
# Open http://localhost:5173
```

## Repository Structure

```
.
├── learning-app/              # Material-UI learning application
│   ├── src/                   # React components (16 files)
│   ├── public/figures/        # 67 PDF charts
│   └── README.md              # App-specific documentation
│
├── react-app/                 # Tailwind interactive playground
│   ├── src/                   # React components + algorithms (26 files)
│   ├── public/figures/        # 67 PDF charts
│   └── README.md              # App-specific documentation
│
├── presentations/             # LaTeX Beamer slides
│   ├── *.tex                  # 6 LaTeX source files
│   └── *.pdf                  # 14 compiled presentations
│
├── figures/                   # 67 Python-generated charts
├── python/                    # 19 chart generation scripts
├── lab/                       # Jupyter notebooks (2 notebooks)
└── docs/                      # Additional documentation
```

## Features

### Learning App
- **3 Structured Learning Goals** with progress tracking
- **62 Educational Slides** organized pedagogically
- **Sidebar Navigation** with visual progress bars
- **Material-UI Design** with purple theme (#3333B2)
- **Progress Persistence** via localStorage

### Interactive Playground
- **Live Algorithm Demonstrations** for all 6 methods
- **Parameter Tuning** with real-time results
- **Side-by-Side Comparison** of different methods
- **Quality Metrics** (repetition rate, distinct-n scores)
- **Preset Configurations** (Factual, Creative, Balanced)

## Decoding Methods Covered

1. **Greedy Decoding** - Always select highest probability (deterministic)
2. **Beam Search** - Maintain top-k sequences (deterministic)
3. **Temperature Sampling** - Reshape distribution for creativity (stochastic)
4. **Top-k Sampling** - Filter to top-k then sample (stochastic)
5. **Nucleus (Top-p)** - Adaptive cumulative probability cutoff (stochastic)
6. **Contrastive Search** - Penalize repetition and similar tokens (deterministic)

## Teaching Materials

### Presentations
- **Canonical Version**: `20251119_1135_week09_improved_readability.pdf` (66 slides)
- **Pedagogical Structure**: Extremes → Toolbox → Problems → Integration
- **LaTeX Source**: Available for customization

### Lab Notebooks
- **Full Lab**: `week09_decoding_lab.ipynb` (comprehensive exercises)
- **Simplified**: `week09_decoding_simplified.ipynb` (beginner-friendly)
- **HTML Export**: For web viewing without Jupyter

### Visualizations
- **67 Professional Charts** in BSc Discovery color scheme
- **Python Scripts**: All generation scripts included
- **Chart Types**: Graphviz diagrams, matplotlib plots, seaborn heatmaps

## Technology Stack

### Learning App
- React 19 + Vite
- Material-UI 7
- Framer Motion (animations)
- react-pdf (PDF viewing)
- Recharts (charting)

### Interactive Playground
- React 18 + Vite
- Tailwind CSS 4
- React Router 7
- D3.js (visualizations)
- Math.js (calculations)

## Development

### Prerequisites
- Node.js 18+ and npm
- Git
- (Optional) Python 3.8+ for chart generation

### Installation
```bash
# Clone repository
git clone git@git.fhgr.ch:digital-finance/Natural-Language-Processing-Decoding-Strategies.git
cd Natural-Language-Processing-Decoding-Strategies

# Install learning-app
cd learning-app
npm install

# Install react-app
cd ../react-app
npm install
```

### Build for Production
```bash
# Learning app
cd learning-app
npm run build
npm run preview

# Interactive playground
cd react-app
npm run build
npm run preview
```

## Educational Design

Based on **BSc Discovery Pedagogy**:
1. **Problem before solution** (slides show extremes first)
2. **Concrete before abstract** (worked examples with actual numbers)
3. **Worked examples** (real decoding scenarios)
4. **Dual-slide pattern** (visual + detail)
5. **Checkpoint quizzes** (3 quizzes at key points)

## Chart Generation

All 67 charts are generated using Python scripts:
```bash
cd python
python generate_week09_enhanced_charts.py
```

## Color Scheme

**BSc Discovery Colors**:
- Purple (`#3333B2`): Primary brand
- Dark Gray (`#404040`): Main text
- Lavender shades: Backgrounds
- Green (`#2CA02C`): Success
- Red (`#D62728`): Error
- Orange (`#FF7F0E`): Warning

## Documentation

- **[learning-app/README.md](learning-app/README.md)** - Learning app features
- **[react-app/README.md](react-app/README.md)** - Playground technical details
- **[docs/COMPLETION_REPORT.md](docs/COMPLETION_REPORT.md)** - Development summary
- **[docs/IMPLEMENTATION_SUMMARY.md](docs/IMPLEMENTATION_SUMMARY.md)** - Technical details

## License

Part of NLP Course 2025 materials. Educational use permitted.

## Course Context

This is **Week 9** of a 12-week NLP course covering:
- Week 1-2: Foundations and embeddings
- Week 3-4: RNN/LSTM and Seq2Seq
- Week 5-7: Transformers and pre-trained models
- **Week 9: Decoding Strategies** ← You are here
- Week 10-12: Fine-tuning, efficiency, ethics

## Authors

- Course Design: Prof. Joerg Osterrieder
- Interactive Apps: AI-assisted development
- Charts: Python matplotlib/seaborn/graphviz

## Support

For issues or questions:
- Check the Wiki for setup guides
- Review app-specific README files
- Contact course instructor

---

**Last Updated**: November 22, 2025
**Version**: 1.0.0
**Status**: Production Ready
