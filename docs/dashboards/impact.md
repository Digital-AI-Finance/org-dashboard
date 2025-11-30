# Research Impact Dashboard

<div class="dashboard-header">
<p class="dashboard-description">
Comprehensive view of research impact metrics across all repositories including h-index, citation counts, publication trends, and reproducibility scores.
</p>
</div>

## Overview Metrics

<div id="metrics-summary" class="metrics-grid">
<div class="metric-card">
<h3>Organization H-Index</h3>
<div id="org-h-index" class="metric-value">-</div>
<p class="metric-description">Academic impact score</p>
</div>
<div class="metric-card">
<h3>Total Publications</h3>
<div id="total-pubs" class="metric-value">-</div>
<p class="metric-description">Across all repositories</p>
</div>
<div class="metric-card">
<h3>Total Citations</h3>
<div id="total-citations" class="metric-value">-</div>
<p class="metric-description">Sum of all publications</p>
</div>
<div class="metric-card">
<h3>Avg Reproducibility</h3>
<div id="avg-repro" class="metric-value">-</div>
<p class="metric-description">Mean score across repos</p>
</div>
</div>

## Filter Options

<div class="dashboard-controls">
<label for="repo-filter">Filter by Repository:</label>
<select id="repo-filter" class="filter-select">
<option value="all">All Repositories</option>
</select>
<button id="reset-filter" class="btn-secondary">Reset Filters</button>
</div>

## Research Impact Metrics

<div class="viz-container">
<div class="viz-header">
<h3>Research Impact by Repository</h3>
<div class="viz-actions">
<button onclick="downloadVisualization('research-impact')" class="btn-download">Download PNG</button>
<button onclick="openFullscreen('research-impact')" class="btn-fullscreen">Fullscreen</button>
</div>
</div>
<iframe id="research-impact"
        src="../visualizations/research_impact.html"
        width="100%"
        height="600px"
        frameborder="0"
        loading="lazy">
</iframe>
<p class="viz-caption">H-index and total citations by repository. Larger bubbles indicate higher publication counts.</p>
</div>

## Reproducibility Assessment

<div class="viz-container">
<div class="viz-header">
<h3>Reproducibility Radar Chart</h3>
<div class="viz-actions">
<button onclick="downloadVisualization('reproducibility')" class="btn-download">Download PNG</button>
<button onclick="openFullscreen('reproducibility')" class="btn-fullscreen">Fullscreen</button>
</div>
</div>
<iframe id="reproducibility"
        src="../visualizations/reproducibility_radar.html"
        width="100%"
        height="600px"
        frameborder="0"
        loading="lazy">
</iframe>
<p class="viz-caption">Multi-dimensional reproducibility scores (Data Availability, Code Quality, Documentation, Environment, Tests).</p>
</div>

## Citation Trends

<div class="viz-container">
<div class="viz-header">
<h3>Citation Trends Over Time</h3>
<div class="viz-actions">
<button onclick="downloadVisualization('citations')" class="btn-download">Download PNG</button>
<button onclick="openFullscreen('citations')" class="btn-fullscreen">Fullscreen</button>
</div>
</div>
<iframe id="citations"
        src="../visualizations/citation_trends.html"
        width="100%"
        height="600px"
        frameborder="0"
        loading="lazy">
</iframe>
<p class="viz-caption">Historical citation accumulation across all publications.</p>
</div>

## Citation Network

<div class="viz-container">
<div class="viz-header">
<h3>Citation Network Graph</h3>
<div class="viz-actions">
<button onclick="downloadVisualization('network')" class="btn-download">Download PNG</button>
<button onclick="openFullscreen('network')" class="btn-fullscreen">Fullscreen</button>
</div>
</div>
<iframe id="network"
        src="../visualizations/citation_network.html"
        width="100%"
        height="700px"
        frameborder="0"
        loading="lazy">
</iframe>
<p class="viz-caption">Network visualization of citation relationships between publications.</p>
</div>

## Download Full Report

<div class="download-section">
<h3>Export Dashboard Data</h3>
<p>Download complete impact metrics and visualizations:</p>
<div class="download-buttons">
<button onclick="downloadReport('pdf')" class="btn-primary">
<span class="icon">PDF</span> Download PDF Report
</button>
<button onclick="downloadReport('csv')" class="btn-primary">
<span class="icon">CSV</span> Download Data (CSV)
</button>
<button onclick="downloadReport('json')" class="btn-primary">
<span class="icon">JSON</span> Download Data (JSON)
</button>
</div>
</div>

<style>
.dashboard-header {
    background: linear-gradient(135deg, #003366 0%, #0056b3 100%);
    color: white;
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
}

.dashboard-description {
    font-size: 1.1rem;
    margin: 0;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.metric-card {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.metric-card h3 {
    margin: 0 0 0.5rem 0;
    font-size: 0.9rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #003366;
    margin: 0.5rem 0;
}

.metric-description {
    font-size: 0.85rem;
    color: #6c757d;
    margin: 0.5rem 0 0 0;
}

.dashboard-controls {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 2rem 0;
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}

.dashboard-controls label {
    font-weight: 600;
    color: #495057;
}

.filter-select {
    padding: 0.5rem 1rem;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 1rem;
    min-width: 200px;
}

.viz-container {
    margin: 3rem 0;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    overflow: hidden;
}

.viz-header {
    background: #f8f9fa;
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #dee2e6;
}

.viz-header h3 {
    margin: 0;
    color: #003366;
}

.viz-actions {
    display: flex;
    gap: 0.5rem;
}

.viz-caption {
    padding: 1rem 1.5rem;
    margin: 0;
    background: #f8f9fa;
    border-top: 1px solid #dee2e6;
    font-size: 0.9rem;
    color: #6c757d;
    font-style: italic;
}

.btn-primary, .btn-secondary, .btn-download, .btn-fullscreen {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-primary {
    background: #003366;
    color: white;
    font-weight: 600;
}

.btn-primary:hover {
    background: #002244;
    transform: translateY(-1px);
}

.btn-secondary {
    background: #6c757d;
    color: white;
}

.btn-secondary:hover {
    background: #5a6268;
}

.btn-download {
    background: #28a745;
    color: white;
    font-size: 0.85rem;
}

.btn-download:hover {
    background: #218838;
}

.btn-fullscreen {
    background: #007bff;
    color: white;
    font-size: 0.85rem;
}

.btn-fullscreen:hover {
    background: #0056b3;
}

.download-section {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 8px;
    margin: 3rem 0;
    text-align: center;
}

.download-section h3 {
    margin-top: 0;
    color: #003366;
}

.download-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}

.icon {
    display: inline-block;
    margin-right: 0.5rem;
    font-weight: bold;
}

@media (max-width: 768px) {
    .dashboard-controls {
        flex-direction: column;
        align-items: stretch;
    }

    .filter-select {
        width: 100%;
    }

    .viz-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }

    .download-buttons {
        flex-direction: column;
    }
}
</style>

<script>
// Load repository data and populate metrics
async function loadDashboardData() {
    try {
        const response = await fetch('../data/repos.json');
        const repos = await response.json();

        // Calculate metrics
        let totalPubs = 0;
        let totalCitations = 0;
        let reproScores = [];
        let hIndices = [];

        repos.forEach(repo => {
            const research = repo.research_metadata?.research || {};
            const pubs = repo.research_metadata?.publications || [];
            const repro = repo.research_metadata?.reproducibility || {};

            totalPubs += pubs.length;

            pubs.forEach(pub => {
                totalCitations += pub.citations || 0;
            });

            if (repro.score) {
                reproScores.push(repro.score);
            }
        });

        // Calculate organization H-index (simplified)
        const citationCounts = [];
        repos.forEach(repo => {
            const pubs = repo.research_metadata?.publications || [];
            pubs.forEach(pub => {
                citationCounts.push(pub.citations || 0);
            });
        });

        citationCounts.sort((a, b) => b - a);
        let hIndex = 0;
        for (let i = 0; i < citationCounts.length; i++) {
            if (citationCounts[i] >= i + 1) {
                hIndex = i + 1;
            } else {
                break;
            }
        }

        const avgRepro = reproScores.length > 0
            ? (reproScores.reduce((a, b) => a + b, 0) / reproScores.length).toFixed(1)
            : 0;

        // Update UI
        document.getElementById('org-h-index').textContent = hIndex;
        document.getElementById('total-pubs').textContent = totalPubs;
        document.getElementById('total-citations').textContent = totalCitations;
        document.getElementById('avg-repro').textContent = avgRepro;

        // Populate repository filter
        const filterSelect = document.getElementById('repo-filter');
        repos.forEach(repo => {
            const option = document.createElement('option');
            option.value = repo.name;
            option.textContent = repo.name;
            filterSelect.appendChild(option);
        });

    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

// Download visualization as PNG
function downloadVisualization(vizId) {
    const iframe = document.getElementById(vizId);
    if (!iframe) return;

    alert(`Download functionality requires the visualization to be accessed directly. Opening in new tab...`);
    window.open(iframe.src, '_blank');
}

// Open visualization in fullscreen
function openFullscreen(vizId) {
    const iframe = document.getElementById(vizId);
    if (!iframe) return;

    if (iframe.requestFullscreen) {
        iframe.requestFullscreen();
    } else if (iframe.webkitRequestFullscreen) {
        iframe.webkitRequestFullscreen();
    } else if (iframe.msRequestFullscreen) {
        iframe.msRequestFullscreen();
    }
}

// Download complete report
function downloadReport(format) {
    const filename = `impact-report.${format}`;

    if (format === 'json') {
        fetch('../data/repos.json')
            .then(r => r.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                a.click();
                URL.revokeObjectURL(url);
            });
    } else if (format === 'csv') {
        alert(`CSV export will be available soon. For now, view data in ../data/repos.json`);
    } else if (format === 'pdf') {
        alert(`PDF export will be available soon. For now, use browser Print > Save as PDF`);
    }
}

// Repository filter handler
document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();

    const filterSelect = document.getElementById('repo-filter');
    filterSelect.addEventListener('change', (e) => {
        const selectedRepo = e.target.value;
        // Filter logic will be implemented when visualizations support URL parameters
        console.log('Filter selected:', selectedRepo);
    });

    document.getElementById('reset-filter').addEventListener('click', () => {
        filterSelect.value = 'all';
        // Reset all visualizations
    });
});
</script>
