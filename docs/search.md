# Advanced Search

<div class="search-container">
<div class="search-header">
<input type="text" id="search-input" placeholder="Search repositories, publications, code..." autocomplete="off">
<button id="search-button" class="btn-search">Search</button>
<button id="clear-search" class="btn-clear">Clear</button>
</div>
<div id="autocomplete-suggestions" class="autocomplete-container"></div>
</div>

<div class="search-layout">
<aside class="facet-panel">
<h3>Filter Results</h3>

<div class="facet-group">
<h4>Document Type</h4>
<div id="filter-type" class="filter-checkboxes"></div>
</div>

<div class="facet-group">
<h4>Repository</h4>
<div id="filter-repo" class="filter-checkboxes"></div>
</div>

<div class="facet-group">
<h4>Language</h4>
<div id="filter-language" class="filter-checkboxes"></div>
</div>

<div class="facet-group">
<h4>Topics</h4>
<div id="filter-topics" class="filter-checkboxes"></div>
</div>

<div class="facet-group">
<h4>Publication Year</h4>
<div id="filter-year" class="filter-checkboxes"></div>
</div>

<div class="facet-actions">
<button id="apply-filters" class="btn-primary">Apply Filters</button>
<button id="reset-filters" class="btn-secondary">Reset All</button>
</div>
</aside>

<main class="search-results">
<div class="results-header">
<div id="results-count" class="results-count">Enter a search query</div>
<div class="sort-controls">
<label for="sort-by">Sort by:</label>
<select id="sort-by" class="sort-select">
<option value="relevance">Relevance</option>
<option value="stars">Stars (High to Low)</option>
<option value="recent">Recently Updated</option>
<option value="title">Title (A-Z)</option>
</select>
</div>
</div>

<div id="search-results" class="results-list">
<!-- Results will be populated here -->
</div>

<div id="pagination" class="pagination">
<!-- Pagination controls will be populated here -->
</div>
</main>
</div>

<style>
.search-container {
position: relative;
margin: 2rem 0;
}

.search-header {
display: flex;
gap: 0.5rem;
}

#search-input {
flex: 1;
padding: 0.75rem 1rem;
font-size: 1rem;
border: 2px solid #003366;
border-radius: 4px;
outline: none;
transition: border-color 0.2s;
}

#search-input:focus {
border-color: #0056b3;
box-shadow: 0 0 0 3px rgba(0,51,102,0.1);
}

.btn-search, .btn-clear {
padding: 0.75rem 1.5rem;
border: none;
border-radius: 4px;
font-size: 1rem;
cursor: pointer;
font-weight: 600;
transition: all 0.2s;
}

.btn-search {
background: #003366;
color: white;
}

.btn-search:hover {
background: #002244;
transform: translateY(-1px);
}

.btn-clear {
background: #6c757d;
color: white;
}

.btn-clear:hover {
background: #5a6268;
}

.autocomplete-container {
position: absolute;
top: 100%;
left: 0;
right: 60px;
background: white;
border: 1px solid #dee2e6;
border-top: none;
border-radius: 0 0 4px 4px;
max-height: 300px;
overflow-y: auto;
z-index: 1000;
display: none;
}

.autocomplete-item {
padding: 0.75rem 1rem;
cursor: pointer;
border-bottom: 1px solid #f1f3f5;
}

.autocomplete-item:hover {
background: #f8f9fa;
}

.search-layout {
display: grid;
grid-template-columns: 280px 1fr;
gap: 2rem;
margin: 2rem 0;
}

.facet-panel {
background: #f8f9fa;
padding: 1.5rem;
border-radius: 8px;
height: fit-content;
position: sticky;
top: 1rem;
}

.facet-panel h3 {
margin: 0 0 1.5rem 0;
color: #003366;
border-bottom: 2px solid #003366;
padding-bottom: 0.5rem;
}

.facet-group {
margin: 1.5rem 0;
}

.facet-group h4 {
margin: 0 0 0.75rem 0;
font-size: 0.9rem;
color: #495057;
text-transform: uppercase;
letter-spacing: 0.5px;
}

.filter-checkboxes {
max-height: 200px;
overflow-y: auto;
}

.filter-checkbox {
display: flex;
align-items: center;
padding: 0.5rem 0;
}

.filter-checkbox input[type="checkbox"] {
margin-right: 0.5rem;
width: 18px;
height: 18px;
cursor: pointer;
}

.filter-checkbox label {
cursor: pointer;
font-size: 0.9rem;
}

.filter-count {
margin-left: auto;
font-size: 0.85rem;
color: #6c757d;
font-weight: 600;
}

.facet-actions {
margin-top: 1.5rem;
display: flex;
flex-direction: column;
gap: 0.5rem;
}

.btn-primary, .btn-secondary {
padding: 0.75rem;
border: none;
border-radius: 4px;
font-size: 0.9rem;
cursor: pointer;
font-weight: 600;
transition: all 0.2s;
}

.btn-primary {
background: #003366;
color: white;
}

.btn-primary:hover {
background: #002244;
}

.btn-secondary {
background: #6c757d;
color: white;
}

.btn-secondary:hover {
background: #5a6268;
}

.results-header {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 1.5rem;
padding-bottom: 1rem;
border-bottom: 2px solid #dee2e6;
}

.results-count {
font-size: 1.1rem;
font-weight: 600;
color: #495057;
}

.sort-controls {
display: flex;
align-items: center;
gap: 0.5rem;
}

.sort-controls label {
font-size: 0.9rem;
color: #6c757d;
}

.sort-select {
padding: 0.5rem;
border: 1px solid #ced4da;
border-radius: 4px;
font-size: 0.9rem;
}

.results-list {
min-height: 400px;
}

.result-item {
background: white;
border: 1px solid #dee2e6;
border-radius: 8px;
padding: 1.5rem;
margin-bottom: 1rem;
transition: all 0.2s;
}

.result-item:hover {
box-shadow: 0 4px 12px rgba(0,0,0,0.1);
transform: translateY(-2px);
border-color: #003366;
}

.result-title {
margin: 0 0 0.5rem 0;
color: #003366;
font-size: 1.2rem;
}

.result-title a {
color: #003366;
text-decoration: none;
}

.result-title a:hover {
text-decoration: underline;
}

.result-metadata {
display: flex;
gap: 1rem;
margin: 0.5rem 0;
flex-wrap: wrap;
}

.result-badge {
display: inline-block;
padding: 0.25rem 0.75rem;
border-radius: 12px;
font-size: 0.75rem;
font-weight: 600;
text-transform: uppercase;
}

.badge-readme { background: #e3f2fd; color: #1976d2; }
.badge-publication { background: #f3e5f5; color: #7b1fa2; }
.badge-research { background: #e8f5e9; color: #388e3c; }
.badge-code { background: #fff3e0; color: #f57c00; }

.result-preview {
margin: 1rem 0;
color: #495057;
line-height: 1.6;
}

.result-stats {
display: flex;
gap: 1.5rem;
font-size: 0.85rem;
color: #6c757d;
margin-top: 1rem;
}

.result-stat {
display: flex;
align-items: center;
gap: 0.25rem;
}

.pagination {
display: flex;
justify-content: center;
gap: 0.5rem;
margin: 2rem 0;
}

.page-btn {
padding: 0.5rem 1rem;
border: 1px solid #dee2e6;
background: white;
border-radius: 4px;
cursor: pointer;
transition: all 0.2s;
}

.page-btn:hover {
background: #f8f9fa;
border-color: #003366;
}

.page-btn.active {
background: #003366;
color: white;
border-color: #003366;
}

.page-btn:disabled {
opacity: 0.5;
cursor: not-allowed;
}

.no-results {
text-align: center;
padding: 3rem;
color: #6c757d;
}

.no-results h3 {
color: #495057;
margin-bottom: 0.5rem;
}

@media (max-width: 968px) {
.search-layout {
grid-template-columns: 1fr;
}

.facet-panel {
position: static;
}

.results-header {
flex-direction: column;
align-items: flex-start;
gap: 1rem;
}
}
</style>

<script>
let searchData = null;
let filteredResults = [];
let currentPage = 1;
const resultsPerPage = 10;
let activeFilters = {
type: new Set(),
repo: new Set(),
language: new Set(),
topics: new Set(),
year: new Set(),
};

// Load search data
async function loadSearchData() {
try {
const response = await fetch('data/search_data_minimal.json');
searchData = await response.json();
console.log('Search data loaded:', searchData.stats);
initializeFacets();
} catch (error) {
console.error('Error loading search data:', error);
document.getElementById('search-results').innerHTML =
'<div class="no-results"><h3>Error loading search data</h3></div>';
}
}

// Initialize facet checkboxes
function initializeFacets() {
if (!searchData) return;

// Document types
const types = searchData.stats.document_types;
renderFacetCheckboxes('filter-type', 'type', types);

// Repositories
const repos = {};
searchData.documents.forEach(doc => {
const repo = doc.metadata.repo;
if (repo) repos[repo] = (repos[repo] || 0) + 1;
});
renderFacetCheckboxes('filter-repo', 'repo', repos);

// Languages
const languages = {};
Object.values(searchData.repos).forEach(repo => {
if (repo.language) {
languages[repo.language] = (languages[repo.language] || 0) + 1;
}
});
renderFacetCheckboxes('filter-language', 'language', languages);

// Topics
const topics = {};
Object.values(searchData.repos).forEach(repo => {
if (repo.topics) {
repo.topics.forEach(topic => {
topics[topic] = (topics[topic] || 0) + 1;
});
}
});
renderFacetCheckboxes('filter-topics', 'topics', topics);

// Years
const years = {};
searchData.documents.forEach(doc => {
const year = doc.metadata.year;
if (year) years[year] = (years[year] || 0) + 1;
});
renderFacetCheckboxes('filter-year', 'year', years);
}

function renderFacetCheckboxes(containerId, facetName, counts) {
const container = document.getElementById(containerId);
const sortedEntries = Object.entries(counts).sort((a, b) => b[1] - a[1]);

container.innerHTML = sortedEntries.map(([value, count]) => `
<div class="filter-checkbox">
<input type="checkbox" id="${facetName}-${value}" value="${value}" data-facet="${facetName}">
<label for="${facetName}-${value}">${value}</label>
<span class="filter-count">(${count})</span>
</div>
`).join('');

// Add event listeners
container.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
checkbox.addEventListener('change', updateActiveFilters);
});
}

function updateActiveFilters() {
// Reset active filters
Object.keys(activeFilters).forEach(key => activeFilters[key].clear());

// Collect checked filters
document.querySelectorAll('.filter-checkbox input:checked').forEach(checkbox => {
const facet = checkbox.dataset.facet;
const value = checkbox.value;
activeFilters[facet].add(value);
});
}

// Search functionality
function performSearch() {
const query = document.getElementById('search-input').value.trim();

if (!query) {
document.getElementById('search-results').innerHTML =
'<div class="no-results"><h3>Please enter a search query</h3></div>';
document.getElementById('results-count').textContent = 'Enter a search query';
return;
}

// Tokenize query
const queryTokens = query.toLowerCase().split(/\s+/).filter(t => t.length > 2);

// Search documents
let results = [];
searchData.documents.forEach(doc => {
const content = doc.content.toLowerCase();
const title = (doc.metadata.title || '').toLowerCase();

// Calculate relevance score
let score = 0;
queryTokens.forEach(token => {
const contentMatches = (content.match(new RegExp(token, 'g')) || []).length;
const titleMatches = (title.match(new RegExp(token, 'g')) || []).length;
score += contentMatches + (titleMatches * 3); // Title matches weighted higher
});

if (score > 0) {
// Apply filters
let passesFilters = true;

// Type filter
if (activeFilters.type.size > 0 && !activeFilters.type.has(doc.metadata.type)) {
passesFilters = false;
}

// Repo filter
if (activeFilters.repo.size > 0 && !activeFilters.repo.has(doc.metadata.repo)) {
passesFilters = false;
}

// Language filter
if (activeFilters.language.size > 0) {
const repo = searchData.repos[doc.metadata.repo];
if (!repo || !activeFilters.language.has(repo.language)) {
passesFilters = false;
}
}

// Topics filter
if (activeFilters.topics.size > 0) {
const repo = searchData.repos[doc.metadata.repo];
if (!repo || !repo.topics || !repo.topics.some(t => activeFilters.topics.has(t))) {
passesFilters = false;
}
}

// Year filter
if (activeFilters.year.size > 0 && !activeFilters.year.has(String(doc.metadata.year))) {
passesFilters = false;
}

if (passesFilters) {
results.push({ doc, score });
}
}
});

filteredResults = results;
sortResults();
currentPage = 1;
displayResults();
}

function sortResults() {
const sortBy = document.getElementById('sort-by').value;

filteredResults.sort((a, b) => {
switch (sortBy) {
case 'relevance':
return b.score - a.score;
case 'stars':
const starsA = searchData.repos[a.doc.metadata.repo]?.stars || 0;
const starsB = searchData.repos[b.doc.metadata.repo]?.stars || 0;
return starsB - starsA;
case 'recent':
const dateA = searchData.repos[a.doc.metadata.repo]?.updated_at || '';
const dateB = searchData.repos[b.doc.metadata.repo]?.updated_at || '';
return dateB.localeCompare(dateA);
case 'title':
const titleA = a.doc.metadata.title || '';
const titleB = b.doc.metadata.title || '';
return titleA.localeCompare(titleB);
default:
return 0;
}
});
}

function displayResults() {
const container = document.getElementById('search-results');
const start = (currentPage - 1) * resultsPerPage;
const end = start + resultsPerPage;
const pageResults = filteredResults.slice(start, end);

// Update count
document.getElementById('results-count').textContent =
`${filteredResults.length} result${filteredResults.length !== 1 ? 's' : ''} found`;

if (pageResults.length === 0) {
container.innerHTML = `
<div class="no-results">
<h3>No results found</h3>
<p>Try adjusting your search query or filters</p>
</div>
`;
document.getElementById('pagination').innerHTML = '';
return;
}

// Render results
container.innerHTML = pageResults.map(result => {
const doc = result.doc;
const meta = doc.metadata;
const repo = searchData.repos[meta.repo] || {};

const typeBadge = `<span class="result-badge badge-${meta.type}">${meta.type}</span>`;
const repoLink = `<a href="repos/${meta.repo}/">${meta.repo}</a>`;

return `
<div class="result-item">
<h3 class="result-title">
<a href="repos/${meta.repo}/">${meta.title || 'Untitled'}</a>
</h3>
<div class="result-metadata">
${typeBadge}
<span>${repoLink}</span>
${repo.language ? `<span>Language: ${repo.language}</span>` : ''}
${meta.year ? `<span>Year: ${meta.year}</span>` : ''}
</div>
<div class="result-preview">${doc.preview}...</div>
<div class="result-stats">
${repo.stars !== undefined ? `<span class="result-stat">Stars: ${repo.stars}</span>` : ''}
${repo.forks !== undefined ? `<span class="result-stat">Forks: ${repo.forks}</span>` : ''}
<span class="result-stat">Relevance: ${result.score.toFixed(1)}</span>
</div>
</div>
`;
}).join('');

// Render pagination
renderPagination();
}

function renderPagination() {
const totalPages = Math.ceil(filteredResults.length / resultsPerPage);

if (totalPages <= 1) {
document.getElementById('pagination').innerHTML = '';
return;
}

let buttons = [];

// Previous button
buttons.push(`
<button class="page-btn" onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
Previous
</button>
`);

// Page numbers
for (let i = 1; i <= totalPages; i++) {
if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
buttons.push(`
<button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="changePage(${i})">
${i}
</button>
`);
} else if (i === currentPage - 3 || i === currentPage + 3) {
buttons.push('<span>...</span>');
}
}

// Next button
buttons.push(`
<button class="page-btn" onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
Next
</button>
`);

document.getElementById('pagination').innerHTML = buttons.join('');
}

function changePage(page) {
const totalPages = Math.ceil(filteredResults.length / resultsPerPage);
if (page < 1 || page > totalPages) return;
currentPage = page;
displayResults();
window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
loadSearchData();

document.getElementById('search-button').addEventListener('click', performSearch);
document.getElementById('search-input').addEventListener('keypress', (e) => {
if (e.key === 'Enter') performSearch();
});

document.getElementById('clear-search').addEventListener('click', () => {
document.getElementById('search-input').value = '';
filteredResults = [];
document.getElementById('search-results').innerHTML = '';
document.getElementById('results-count').textContent = 'Enter a search query';
document.getElementById('pagination').innerHTML = '';
});

document.getElementById('apply-filters').addEventListener('click', performSearch);

document.getElementById('reset-filters').addEventListener('click', () => {
document.querySelectorAll('.filter-checkbox input:checked').forEach(cb => cb.checked = false);
Object.keys(activeFilters).forEach(key => activeFilters[key].clear());
performSearch();
});

document.getElementById('sort-by').addEventListener('change', () => {
sortResults();
displayResults();
});
});
</script>
