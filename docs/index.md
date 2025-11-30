# Digital-AI-Finance Research Platform

<div class="hero-section">
<h2>Comprehensive Research Analytics for Academic GitHub Organizations</h2>
<p class="hero-tagline">Automated dashboards, advanced search, and interactive visualizations for research repositories</p>
</div>

---

## Featured Analytics

<div class="viz-grid">
<div class="viz-card">
<a href="visualizations/repository_network.html" class="viz-link">
<div class="viz-preview" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
<h3>Repository Network</h3>
<p>Explore connections between repositories</p>
</div>
</a>
</div>

<div class="viz-card">
<a href="visualizations/code_quality_heatmap.html" class="viz-link">
<div class="viz-preview" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
<h3>Code Quality Heatmap</h3>
<p>Real-time quality scores with Git data</p>
</div>
</a>
</div>

<div class="viz-card">
<a href="visualizations/dependency_treemap.html" class="viz-link">
<div class="viz-preview" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
<h3>Dependency Tree</h3>
<p>Package usage across repositories</p>
</div>
</a>
</div>

<div class="viz-card">
<a href="dashboards/timeseries.html" class="viz-link">
<div class="viz-preview" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
<h3>Time-Series Analytics</h3>
<p>Historical trends and metrics</p>
</div>
</a>
</div>
</div>

---

## Quick Access

<div class="quick-access">
<a href="search/" class="access-btn search-btn">
<span class="icon">🔍</span>
<strong>Advanced Search</strong>
<p>Faceted search with filters</p>
</a>

<a href="dashboards/impact/" class="access-btn impact-btn">
<span class="icon">📊</span>
<strong>Impact Dashboard</strong>
<p>H-index, citations, reproducibility</p>
</a>

<a href="dashboards/timeseries/" class="access-btn timeseries-btn">
<span class="icon">📈</span>
<strong>Time-Series</strong>
<p>Commits, contributors, trends</p>
</a>

<a href="visualizations/repository_overview.html" class="access-btn gallery-btn">
<span class="icon">🎨</span>
<strong>Repository Gallery</strong>
<p>Interactive visual browser</p>
</a>
</div>

---

## Organization Metrics

<div class="metrics-grid">
<div class="metric-box">
<div class="metric-value">13</div>
<div class="metric-label">Total Repositories</div>
</div>
<div class="metric-box">
<div class="metric-value">15</div>
<div class="metric-label">Contributors</div>
</div>
<div class="metric-box">
<div class="metric-value">6</div>
<div class="metric-label">Languages</div>
</div>
<div class="metric-box">
<div class="metric-value">100%</div>
<div class="metric-label">Active Repos</div>
</div>
</div>

---

## Research Topics Discovery

Explore the research landscape through machine learning-discovered topics. Each bubble represents a topic cluster.

<div class="topic-viz-container">
<iframe src="visualizations/landing_topic_bubbles.html" width="100%" height="600" frameborder="0"></iframe>
<div class="viz-controls">
<a href="visualizations/landing_topic_bubbles_lda.html">LDA Topics</a> |
<a href="visualizations/landing_topic_bubbles_2d.html">2D Version</a>
</div>
</div>

---

## Top Languages

| Language | Repositories |
|----------|--------------|
| [Python](by-language/python.md) | 3 |
| [TeX](by-language/tex.md) | 3 |
| [Jupyter Notebook](by-language/jupyter-notebook.md) | 2 |
| [HTML](by-language/html.md) | 1 |
| [JavaScript](by-language/javascript.md) | 1 |

[View all languages](by-language/index.md){ .md-button }

---

## Top Topics

| Topic | Repositories |
|-------|--------------|
| [finance](by-topic/finance.md) | 3 |
| [machine-learning](by-topic/machine-learning.md) | 1 |
| [portfolio-optimization](by-topic/portfolio-optimization.md) | 1 |
| [reinforcement-learning](by-topic/reinforcement-learning.md) | 1 |
| [credit-risk](by-topic/credit-risk.md) | 1 |

[View all topics](by-topic/index.md){ .md-button }

---

## Recently Active Repositories

| Repository | Last Push |
|------------|-----------|
| [org-dashboard](repos/org-dashboard.md) | 2025-11-28 |
| [Natural-Language-Processing](repos/Natural-Language-Processing.md) | 2025-11-23 |
| [Green-Finance](repos/Green-Finance.md) | 2025-11-18 |
| [ShareBuybacks](repos/ShareBuybacks.md) | 2025-11-18 |
| [quantlet-branding-tools](repos/quantlet-branding-tools.md) | 2025-11-17 |

---

<div class="footer-cta">
<h3>About This Platform</h3>
<p>Automated research analytics powered by GitHub Actions. Updated daily with the latest repository data, publication metrics, and code quality assessments.</p>
<p><strong>Last updated:</strong> 2025-11-30</p>
</div>

<style>
.hero-section {
    background: linear-gradient(135deg, #003366 0%, #0056b3 100%);
    color: white;
    padding: 3rem 2rem;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 2rem;
}

.hero-section h2 {
    margin: 0 0 1rem 0;
    font-size: 2rem;
    color: white;
}

.hero-tagline {
    font-size: 1.2rem;
    margin: 0;
    opacity: 0.95;
}

.viz-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.viz-card {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}

.viz-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0,0,0,0.2);
}

.viz-link {
    text-decoration: none;
    color: white;
}

.viz-preview {
    padding: 2rem;
    color: white;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.viz-preview h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.4rem;
    color: white;
}

.viz-preview p {
    margin: 0;
    opacity: 0.9;
}

.quick-access {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.access-btn {
    background: white;
    border: 2px solid #dee2e6;
    border-radius: 8px;
    padding: 1.5rem;
    text-decoration: none;
    color: #003366;
    transition: all 0.2s;
    display: block;
    text-align: center;
}

.access-btn:hover {
    border-color: #003366;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.access-btn .icon {
    font-size: 2rem;
    display: block;
    margin-bottom: 0.5rem;
}

.access-btn strong {
    display: block;
    font-size: 1.1rem;
    margin-bottom: 0.25rem;
    color: #003366;
}

.access-btn p {
    margin: 0;
    font-size: 0.9rem;
    color: #6c757d;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.metric-box {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 1.5rem;
    border-radius: 8px;
    text-align: center;
    border: 1px solid #dee2e6;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #003366;
    margin-bottom: 0.5rem;
}

.metric-label {
    font-size: 0.9rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.topic-viz-container {
    border: 1px solid #dee2e6;
    border-radius: 8px;
    overflow: hidden;
    margin: 1rem 0;
}

.viz-controls {
    background: #f8f9fa;
    padding: 0.75rem;
    text-align: center;
    font-size: 0.9rem;
    border-top: 1px solid #dee2e6;
}

.viz-controls a {
    color: #003366;
    text-decoration: none;
    margin: 0 0.5rem;
}

.viz-controls a:hover {
    text-decoration: underline;
}

.footer-cta {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    margin: 3rem 0 1rem 0;
}

.footer-cta h3 {
    color: #003366;
    margin-top: 0;
}

.footer-cta p {
    color: #6c757d;
    margin: 0.5rem 0;
}

@media (max-width: 768px) {
    .hero-section h2 {
        font-size: 1.5rem;
    }

    .hero-tagline {
        font-size: 1rem;
    }

    .viz-grid {
        grid-template-columns: 1fr;
    }

    .quick-access {
        grid-template-columns: 1fr;
    }
}
</style>
