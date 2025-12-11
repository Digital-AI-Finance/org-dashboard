# digital-finance

BSc-level Digital Finance course: 48 lessons on FinTech, Blockchain, AI/ML, and Traditional Finance

[View on GitHub](https://github.com/Digital-AI-Finance/digital-finance){ .md-button .md-button--primary }
[Homepage](https://digital-ai-finance.github.io/digital-finance){ .md-button }

---





## Information

| Property | Value |
|----------|-------|
| Language | Python |
| Stars | 0 |
| Forks | 0 |
| Watchers | 0 |
| Open Issues | 0 |
| License | Other |
| Created | 2025-12-07 |
| Last Updated | 2025-12-10 |
| Last Push | 2025-12-10 |
| Contributors | 1 |
| Default Branch | main |
| Visibility | public |


## Topics

`blockchain` `course-materials` `digital-finance` `education` `fintech` `latex` `machine-learning` `python` `beamer-slides` `course` `finance` `python-demos` 







## Reproducibility


This repository includes reproducibility tools:


- Python requirements.txt













## Status





- Issues: Enabled
- Wiki: Enabled
- Pages: Enabled

## README

# Digital Finance

A comprehensive BSc-level course covering 48 lessons across Fintech, Blockchain, AI/ML, and Traditional Finance.

## Course Overview

This course provides a modern, quantitative approach to digital finance, combining theoretical foundations with practical applications. Students explore cutting-edge technologies transforming financial services while mastering traditional finance concepts.

## Course Structure

### Module 1: Fintech Foundations (12 lessons)
Introduction to financial technology, digital payments, lending platforms, insurtech, regtech, and the evolution of financial services in the digital age.

### Module 2: Blockchain & Cryptocurrencies (12 lessons)
Deep dive into distributed ledger technology, consensus mechanisms, smart contracts, DeFi protocols, tokenomics, and blockchain applications in finance.

### Module 3: AI & Machine Learning in Finance (12 lessons)
Machine learning techniques for financial applications including prediction, classification, natural language processing, reinforcement learning, and ethical AI considerations.

### Module 4: Traditional Finance Fundamentals (12 lessons)
Core concepts in corporate finance, asset pricing, portfolio theory, risk management, derivatives, and quantitative finance methods.

## Quick Start

### Viewing Slides

**Option 1: Pre-compiled PDFs (Recommended)**
- Browse compiled slides in `docs/slides/module_XX/` or `slides/module_XX/`
- View online at GitHub Pages: [https://digital-ai-finance.github.io/digital-finance](https://digital-ai-finance.github.io/digital-finance)

**Option 2: Compile from Source**
```bash
cd slides/module_01_fintech
pdflatex lesson_01_intro_fintech.tex
```

### Running Demos

Python demonstrations are in the `demos/` folder:

```bash
cd demos
pip install -r requirements.txt
python run_all_demos.py
```

Or run individual demos:
```bash
cd demos/module_01_fintech/payment_cost_calculator
python payment_cost_calculator.py
```

### Generating Charts

Chart scripts are in the `charts/` folder:

```bash
cd charts/module_02_blockchain/blockchain_structure
python blockchain_structure.py
```

## Requirements

- Python 3.8+ (for demos and chart generation)
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX) - for compiling slides
- Git for version control

## Repository Structure

```
digital-finance/
├── module_01_fintech/          # Source: FinTech lessons + charts
├── module_02_blockchain/       # Source: Blockchain lessons + charts
├── module_03_ai_ml/            # Source: AI/ML lessons
├── module_04_traditional/      # Source: Traditional finance lessons
├── slides/                     # Organized lesson files
│   ├── module_01_fintech/      # 12 lessons (TEX + PDF)
│   ├── module_02_blockchain/   # 12 lessons (TEX + PDF)
│   ├── module_03_ai_ml/        # 12 lessons (TEX + PDF)
│   └── module_04_traditional/  # 12 lessons (TEX + PDF)
├── docs/                       # GitHub Pages website
│   ├── index.html              # Course homepage
│   └── slides/                 # PDFs for online viewing
├── demos/                      # Python demonstration scripts
├── charts/                     # Chart generation scripts
├── assessments/                # Rubrics and project guidelines
├── syllabus/                   # Course syllabus
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── LICENSE                     # CC BY-NC-SA 4.0
```

**Note:** Module folders contain source files with embedded charts. The `slides/` folder contains organized copies for easy access.

## License

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).

You are free to:
- Share: copy and redistribute the material
- Adapt: remix, transform, and build upon the material

Under the following terms:
- Attribution: give appropriate credit
- NonCommercial: not for commercial purposes
- ShareAlike: distribute under the same license

## Citation

If you use this course material in your research or teaching, please cite:

```bibtex
@misc{digitalfinance2025,
  title={Digital Finance: A Comprehensive Course},
  author={FHGR Digital Finance Team},
  year={2025},
  publisher={GitHub},
  howpublished={\url{https://github.com/Digital-AI-Finance/digital-finance}},
  note={CC BY-NC-SA 4.0}
}
```

## Contributing

This is an educational resource maintained by the Digital Finance team at FHGR. Issues and suggestions are welcome via GitHub Issues.

## Contact

For questions or collaboration inquiries, please open an issue or contact the course team through the Digital-AI-Finance organization.
