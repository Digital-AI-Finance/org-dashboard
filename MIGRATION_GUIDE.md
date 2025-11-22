# Migration Guide: From Scripts to Production Architecture

## Overview

This guide provides step-by-step instructions for migrating from the current script-based architecture to the new production-ready platform architecture.

## Migration Phases

### Phase 1: Prepare Environment (Week 1)

#### 1.1 Set Up New Directory Structure

```bash
# Create new directory structure
mkdir -p src/research_platform/{core,config,models,fetchers,analyzers,generators,utils}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p configs
mkdir -p logs
```

#### 1.2 Install Additional Dependencies

```bash
# Add to requirements.txt
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
pytest-mock>=3.11.1
aiofiles>=23.2.1
redis>=5.0.0  # optional
pydantic>=2.0.0  # for validation
```

#### 1.3 Create Configuration Files

```bash
# Copy provided configuration templates
cp configs/production.yaml.example configs/production.yaml
cp configs/development.yaml.example configs/development.yaml

# Set up environment variables
cp .env.example .env
```

### Phase 2: Core Infrastructure (Week 1-2)

#### 2.1 Migrate Core Components

Map existing scripts to new architecture:

| Current Script | New Module | Notes |
|---------------|------------|-------|
| `build_research_platform.py` | `core/orchestrator.py` | Extract orchestration logic |
| Pipeline phases | `core/phase.py` | Create Phase implementations |
| Error handling | `core/exceptions.py` | Centralize exceptions |

**Migration Steps:**

1. Extract orchestration logic:
```python
# OLD: build_research_platform.py
class ResearchPlatformBuilder:
    def run_phase(self, phase_name, phase_func, *args):
        # Direct function call
        result = phase_func(*args)

# NEW: core/orchestrator.py
class PipelineOrchestrator:
    async def execute_pipeline(self):
        # Phase-based execution with dependency injection
        for phase in self.phases:
            result = await phase.run(self.context)
```

2. Convert functions to Phase classes:
```python
# OLD: Direct function
def fetch_data():
    repos = fetch_from_github()
    return repos

# NEW: Phase class
class FetchDataPhase(Phase):
    async def execute(self, context):
        fetcher = self.get_dependency("github_fetcher")
        repos = await fetcher.fetch_repositories()
        return {"repositories": repos}
```

### Phase 3: Data Models (Week 2)

#### 3.1 Create Domain Models

Convert dictionaries to typed models:

```python
# OLD: Dictionary-based
repo_data = {
    "name": repo.name,
    "stars": repo.stargazers_count,
    "language": repo.language
}

# NEW: Model-based
from research_platform.models.repository import Repository
repo = Repository.from_github(github_repo)
```

#### 3.2 Migrate Data Processing

Update all data processing to use models:

```python
# OLD: scripts/ml_topic_modeling.py
def analyze_repository_topics(repos_data):
    for repo_dict in repos_data:
        readme = repo_dict.get('readme_content', '')

# NEW: analyzers/topic_modeling.py
class TopicAnalyzer(Analyzer):
    async def analyze(self, repositories: List[Repository]):
        for repo in repositories:
            readme = repo.metadata.get('readme_content', '')
```

### Phase 4: Fetchers Migration (Week 2)

#### 4.1 Extract Fetching Logic

Separate API calls from processing:

```python
# OLD: fetch_org_data_research.py
def fetch_repo_data(repo):
    # Mixed fetching and processing
    readme_content = repo.get_readme()
    contributors = repo.get_contributors()
    # Process inline
    return processed_data

# NEW: fetchers/github_fetcher.py
class GitHubFetcher(RepositoryFetcher):
    async def fetch_repository_details(self, repo: Repository):
        # Pure fetching with caching
        async with self.cache.context(repo.id):
            readme = await self._fetch_readme(repo)
            contributors = await self._fetch_contributors(repo)
        return repo
```

#### 4.2 Add Caching Layer

```python
# NEW: fetchers/cache.py
class AsyncCache:
    async def get_or_fetch(self, key, fetch_func):
        cached = await self.get(key)
        if cached:
            return cached

        result = await fetch_func()
        await self.set(key, result)
        return result
```

### Phase 5: Testing Infrastructure (Week 2-3)

#### 5.1 Write Tests for New Components

Start with critical paths:

```bash
# Run tests during migration
pytest tests/unit/test_models/  # Test models first
pytest tests/unit/test_core/     # Test orchestration
pytest tests/integration/        # Test full pipeline
```

#### 5.2 Create Test Fixtures

```python
# tests/fixtures/mock_data.py
def create_mock_repository():
    return Repository(
        id=123,
        name="test-repo",
        full_name="org/test-repo"
    )

# Use in tests
def test_analyzer(mock_repository):
    analyzer = CodeQualityAnalyzer()
    result = analyzer.analyze(mock_repository)
    assert result.score > 0
```

### Phase 6: Async Conversion (Week 3)

#### 6.1 Convert to Async Operations

```python
# OLD: Synchronous
def fetch_all_repos(org_name):
    repos = []
    for page in github.get_org(org_name).get_repos():
        repos.append(fetch_repo_data(page))
    return repos

# NEW: Asynchronous
async def fetch_all_repos(org_name):
    async with AsyncGitHubClient() as client:
        repos = await client.fetch_repositories(org_name)

        # Parallel detail fetching
        tasks = [fetch_repo_details(repo) for repo in repos]
        return await asyncio.gather(*tasks)
```

#### 6.2 Update Pipeline for Async

```python
# Update main entry point
async def main():
    settings = Settings.from_yaml(Path("configs/production.yaml"))
    orchestrator = PipelineOrchestrator(settings)

    # Register phases
    orchestrator.register_phase(FetchDataPhase(settings))
    orchestrator.register_phase(AnalysisPhase(settings))

    # Run pipeline
    result = await orchestrator.execute_pipeline()

if __name__ == "__main__":
    asyncio.run(main())
```

### Phase 7: Gradual Cutover (Week 3-4)

#### 7.1 Parallel Running

Run both old and new systems in parallel:

```python
# Temporary wrapper script
async def run_migration_test():
    # Run old pipeline
    old_result = run_old_pipeline()

    # Run new pipeline
    new_result = await run_new_pipeline()

    # Compare results
    compare_outputs(old_result, new_result)
```

#### 7.2 Feature Flag Migration

Use feature flags for gradual rollout:

```yaml
# configs/production.yaml
migration:
  use_new_fetcher: false
  use_new_analyzer: false
  use_async_pipeline: false
```

```python
if settings.migration.use_new_fetcher:
    fetcher = AsyncGitHubFetcher()
else:
    fetcher = LegacyFetcher()
```

### Phase 8: Deployment Updates (Week 4)

#### 8.1 Update GitHub Actions

```yaml
# .github/workflows/rebuild-platform.yml
- name: Run platform build
  run: |
    if [ "$USE_NEW_ARCHITECTURE" = "true" ]; then
      python -m research_platform build --config configs/production.yaml
    else
      python scripts/build_research_platform.py
    fi
```

#### 8.2 Update Documentation

Create new documentation:
- API documentation
- Architecture diagrams
- Operation guides
- Troubleshooting guides

## Validation Checklist

### Pre-Migration
- [ ] All tests passing on current system
- [ ] Backup of current data
- [ ] Performance baseline recorded

### During Migration
- [ ] Unit tests for each new component
- [ ] Integration tests passing
- [ ] Performance tests show no regression
- [ ] Parallel validation successful

### Post-Migration
- [ ] All features working
- [ ] Performance improved or maintained
- [ ] Documentation updated
- [ ] Team trained on new architecture

## Rollback Plan

If issues arise during migration:

1. **Immediate Rollback**
   ```bash
   # Revert to old pipeline
   git checkout main
   python scripts/build_research_platform.py
   ```

2. **Data Recovery**
   ```bash
   # Restore from backup
   cp -r backups/data-$(date +%Y%m%d)/* data/
   ```

3. **Partial Rollback**
   - Use feature flags to disable problematic components
   - Keep working components from new architecture

## Common Migration Issues

### Issue 1: Import Errors
**Problem**: Scripts can't find new modules
**Solution**:
```bash
# Add src to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or install as package
pip install -e .
```

### Issue 2: Async Compatibility
**Problem**: Mixing sync and async code
**Solution**:
```python
# Use sync_to_async wrapper
from asgiref.sync import sync_to_async

async def hybrid_function():
    result = await sync_to_async(old_sync_function)()
    return result
```

### Issue 3: Configuration Mismatch
**Problem**: Old scripts expect different config format
**Solution**:
```python
# Create compatibility layer
class ConfigAdapter:
    def __init__(self, new_config):
        self.new_config = new_config

    @property
    def GITHUB_TOKEN(self):
        return self.new_config.github.token
```

## Performance Optimization Tips

1. **Use Connection Pooling**
   ```python
   # For API requests
   async with aiohttp.ClientSession() as session:
       # Reuse session for multiple requests
   ```

2. **Implement Caching**
   ```python
   @cache.memoize(ttl=3600)
   async def expensive_operation():
       # Cached for 1 hour
   ```

3. **Batch Operations**
   ```python
   # Process in batches
   for batch in chunks(repositories, 10):
       await process_batch(batch)
   ```

## Monitoring Migration Progress

Track these metrics during migration:

- **Code Coverage**: Should increase to >80%
- **Performance**: API calls/minute, processing time
- **Error Rate**: Should decrease with new error handling
- **Memory Usage**: Should remain stable or improve

## Support and Resources

- **Documentation**: `/docs/architecture/`
- **Examples**: `/examples/migration/`
- **Issues**: GitHub Issues with `migration` label
- **Team Chat**: `#platform-migration` channel

## Timeline Summary

| Week | Phase | Deliverable |
|------|-------|------------|
| 1 | Setup & Core | New structure, core modules |
| 2 | Models & Fetchers | Domain models, API abstraction |
| 3 | Async & Testing | Async pipeline, test coverage |
| 4 | Cutover & Deploy | Production deployment |

## Success Criteria

Migration is complete when:

1. All tests pass (>80% coverage)
2. Performance meets or exceeds baseline
3. No data loss or corruption
4. Team trained on new system
5. Documentation complete
6. Monitoring in place

Remember: This is an iterative process. Start small, test thoroughly, and gradually expand the migration scope.