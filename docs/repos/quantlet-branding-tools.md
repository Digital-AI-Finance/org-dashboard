# quantlet-branding-tools

Automated tools for adding QuantLet branding (logo, QR codes, clickable URLs) to LaTeX Beamer presentations

[View on GitHub](https://github.com/Digital-AI-Finance/quantlet-branding-tools){ .md-button .md-button--primary }


---





## Information

| Property | Value |
|----------|-------|
| Language | Python |
| Stars | 0 |
| Forks | 0 |
| Watchers | 0 |
| Open Issues | 0 |
| License | MIT License |
| Created | 2025-11-28 |
| Last Updated | 2025-11-30 |
| Last Push | 2025-11-30 |
| Contributors | 1 |
| Default Branch | master |
| Visibility | private |






## Datasets

This repository includes 1 dataset(s):

| Dataset | Format | Size |
|---------|--------|------|

| [branding_config.json](https://github.com/Digital-AI-Finance/quantlet-branding-tools/blob/master/utils/branding_config.json) | .json | 0.54 KB |




## Reproducibility


No specific reproducibility files found.







## Status





- Issues: Enabled
- Wiki: Disabled
- Pages: Disabled

## README

# QuantLet LaTeX Branding Tools

Automated tools for adding QuantLet branding (logo, QR codes, clickable URLs) to LaTeX Beamer presentations. Add professional GitHub links to all your chart slides with just 3 commands!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Note:** This is a private repository. For public access, use the GitLab mirror at git.fhgr.ch/digital-finance/quantlet-branding-tools

## 🚀 Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/Digital-AI-Finance/quantlet-branding-tools.git

# 2. Copy to your project
cp -r quantlet-branding-tools /path/to/your/latex/project/

# 3. Run the 3-step process
python generate_qr_codes.py
python add_latex_branding.py
pdflatex your_slides.tex
```

**Result:** All chart slides now have logo + QR code + clickable URL!

---

## 📖 Documentation

Start here based on your needs:

| Document | Purpose | Best For |
|----------|---------|----------|
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | One-page cheat sheet | Quick lookup, already used these tools |
| **[BRANDING_GUIDE.md](BRANDING_GUIDE.md)** | Complete step-by-step tutorial | First time using, new project setup |
| **[TOOLS_REFERENCE.md](TOOLS_REFERENCE.md)** | Detailed technical documentation | Understanding internals, customization |

---

## ✨ Features

- **Automatic URL Generation**: Creates GitHub links from chart folder names
- **LaTeX-Level Branding**: Logo and QR codes added at compile time (not embedded in chart PDFs)
- **Clickable Elements**: Logo, QR code, and URL text all link to GitHub
- **Professional Appearance**:
  - Logo: Fully visible (100% opacity)
  - QR Code: Slightly transparent (80% opacity)
  - Bottom-right positioning
- **Multiple Repository Support**: Sync between main repo and QuantLet mirror
- **Zero Code Changes**: Works with existing chart PDFs

---

## 📁 What This Repository Contains

```
quantlet-branding-tools/
├── add_latex_branding.py          # Main script - adds branding to .tex files
├── remove_duplicate_branding.py   # Remove all branding blocks
├── sync_to_quantlet.py            # Sync to QuantLet repo with updated URLs
├── generate_qr_codes_template.py  # Template for generating QR codes
├── generate_metainfo.py            # Generate metainfo.txt files
├── regenerate_all_charts.py        # Regenerate chart PDFs
├── remove_chart_branding.py        # Remove embedded branding from charts
├── logo/
│   └── quantlet.png               # QuantLet logo (transparent PNG)
├── utils/                          # Legacy embedded branding utilities
├── example/                        # Example project structure
├── README.md                       # This file
├── QUICK_REFERENCE.md             # One-page quick reference
├── BRANDING_GUIDE.md              # Complete tutorial
└── TOOLS_REFERENCE.md             # Technical reference
```

---

## 🎯 Use Cases

### **For Academic Presentations**
Add QuantLet branding to all your Beamer slides with charts:
- Automatic GitHub links for reproducibility
- QR codes for easy access during talks
- Professional appearance for conferences

### **For Research Repositories**
Make your research more discoverable:
- Link each chart to its source code on GitHub
- Audience can scan QR codes to access code instantly
- Maintain two versions (main repo + QuantLet) with different URLs

### **For Teaching Materials**
Help students find resources:
- Each slide links to the code that generated it
- Students can explore the repository during/after class
- Easy to update URLs when moving between repositories

---

## 🛠️ Installation & Setup

### **Requirements**

- Python 3.6+
- LaTeX packages: `tikz`, `hyperref`, `graphicx`
- Optional: `qrcode` Python package (for QR code generation)

### **Quick Install**

```bash
# Install QR code generator (optional but recommended)
pip install qrcode[pil]

# Clone this repository
git clone https://github.com/Digital-AI-Finance/quantlet-branding-tools.git

# Copy to your project
cp -r quantlet-branding-tools/* /path/to/your/project/
```

---

## 📚 Usage

### **Basic Workflow (3 Steps)**

**1. Generate QR Codes**
```bash
python generate_qr_codes.py
```
This reads `CHART_METADATA['url']` from each chart's Python script and generates QR codes.

**2. Add Branding to LaTeX**
```bash
python add_latex_branding.py
```
This adds tikz overlays with logo + QR + URL to all chart frames in your .tex file.

**3. Compile PDF**
```bash
pdflatex your_slides.tex
```

Done! Your slides now have QuantLet branding.

---

### **Project Structure Requirements**

Your LaTeX project should have this structure:

```
your_project/
├── 01_chart_name/
│   ├── chart_script.py        # Must contain CHART_METADATA
│   ├── chart.pdf
│   └── qr_code.png            # Auto-generated by step 1
├── 02_another_chart/
│   ├── script.py
│   ├── chart.pdf
│   └── qr_code.png
├── slides.tex                  # Your main LaTeX file
├── generate_qr_codes.py        # Copy from generate_qr_codes_template.py
└── add_latex_branding.py       # From this repository
```

**Each chart script must have:**
```python
CHART_METADATA = {
    'title': 'Chart Title',
    'url': 'https://github.com/YourOrg/repo/tree/main/01_chart_name'
}
```

See `example/` directory for a complete working example.

---

## 🎨 Customization

Edit `add_latex_branding.py` to customize:

| Element | Current Value | How to Change |
|---------|---------------|---------------|
| Logo size | `width=0.8cm` | Line 100: Change width |
| Logo opacity | `opacity=1.0` (fully visible) | Line 99: Change opacity (0.0-1.0) |
| QR size | `width=0.6cm` | Line 104: Change width |
| QR opacity | `opacity=0.8` (20% transparent) | Line 103: Change opacity |
| Position | Bottom-right corner | Lines 99, 103, 107: Adjust xshift/yshift |
| Font size | `\tiny` | Line 108: Change to `\scriptsize`, `\footnotesize`, etc. |

---

## 🔄 Syncing to QuantLet Repository

If you maintain both a main repository and a QuantLet mirror:

```bash
python sync_to_quantlet.py
```

This script automatically:
1. Clones/updates the QuantLet repository
2. Copies all files
3. Updates all URLs to point to QuantLet
4. Regenerates QR codes
5. Prepares for commit

See [BRANDING_GUIDE.md](BRANDING_GUIDE.md) for details.

---

## 📖 Examples

### **Before**
```latex
\begin{frame}{Loss Landscape}
  \includegraphics[width=0.95\textwidth]{07_loss_landscape/chart.pdf}
\end{frame}
```

### **After** (automatically added)
```latex
\begin{frame}{Loss Landscape}
  \includegraphics[width=0.95\textwidth]{07_loss_landscape/chart.pdf}

  % Quantlet branding (auto-generated)
  \begin{tikzpicture}[remember picture,overlay]
    % Logo (clickable, fully visible)
    \node[...] {\href{https://github.com/...}{\includegraphics{logo/quantlet.png}}};
    % QR Code (clickable, slightly transparent)
    \node[...] {\href{https://github.com/...}{\includegraphics{qr_code.png}}};
    % URL text (clickable)
    \node[...] {\href{https://github.com/...}{\texttt{07\_loss\_landscape}}};
  \end{tikzpicture}
\end{frame}
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Logo not showing | Check `logo/quantlet.png` exists |
| QR codes missing | Run `python generate_qr_codes.py` |
| Duplicate branding | Run `python remove_duplicate_branding.py` then re-add |
| Wrong repository URLs | Edit CHART_METADATA in chart scripts |
| Compilation errors | Ensure `tikz` and `hyperref` packages are installed |

See [BRANDING_GUIDE.md](BRANDING_GUIDE.md) for complete troubleshooting.

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with example project
5. Submit a pull request

---

## 📄 License

MIT License - Free to use and modify

---

## 🔗 Links

- **GitHub (Private)**: https://github.com/Digital-AI-Finance/quantlet-branding-tools
  - Visibility: Private (Digital-AI-Finance organization members only)
  - Primary development repository
- **GitLab (Private Mirror)**: git.fhgr.ch/digital-finance/quantlet-branding-tools
  - Visibility: Private (Digital Finance group members only)
  - Auto-syncs from GitHub
- **QuantLet**: https://quantlet.de
- **Documentation**: See BRANDING_GUIDE.md and GITLAB_SETUP.md

---

## 💡 Tips

1. **Keep chart PDFs clean**: Don't embed branding in chart images
2. **Use CHART_METADATA**: Always add URLs to your chart scripts
3. **Test before presenting**: Verify all links work
4. **Use version control**: Commit before adding branding (easy to revert)
5. **Reuse this repo**: Clone once, use in many projects

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check the documentation in `BRANDING_GUIDE.md`
- See examples in `example/` directory

---

**Made with ❤️ for the QuantLet community**
