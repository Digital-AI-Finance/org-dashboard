# Time-Series Analytics Dashboard

<div class="dashboard-header">
<p class="dashboard-description">
Historical trends and metrics across all repositories, showing commit activity, contributor growth, and popularity metrics over time.
</p>
</div>

## Commit Activity

<div class="viz-container">
<iframe src="../visualizations/timeseries_commits.html" width="100%" height="550px" frameborder="0"></iframe>
<p class="viz-caption">Daily commit frequency with 7-day moving average trend line.</p>
</div>

## Contributor Growth

<div class="viz-container">
<iframe src="../visualizations/timeseries_contributors.html" width="100%" height="550px" frameborder="0"></iframe>
<p class="viz-caption">Cumulative growth of unique contributors over time.</p>
</div>

## Repository Popularity

<div class="viz-container">
<iframe src="../visualizations/timeseries_stars_forks.html" width="100%" height="550px" frameborder="0"></iframe>
<p class="viz-caption">Current stars and forks comparison across repositories.</p>
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

.viz-container {
    margin: 2rem 0;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    overflow: hidden;
}

.viz-caption {
    padding: 1rem;
    margin: 0;
    background: #f8f9fa;
    border-top: 1px solid #dee2e6;
    font-size: 0.9rem;
    color: #6c757d;
    font-style: italic;
}
</style>
