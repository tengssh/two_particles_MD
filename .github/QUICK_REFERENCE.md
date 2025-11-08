# CI/CD Quick Reference Card

## 🚀 Common Commands

### Local Testing (Before Push)

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=md_simulation --cov-report=term

# Run specific test file
pytest tests/test_particle.py -v

# Run specific test function
pytest tests/test_particle.py::test_kinetic_energy_moving_particle

# Stop at first failure
pytest tests/ -x

# Show print statements
pytest tests/ -s

# Run only failed tests from last run
pytest tests/ --lf
```

### Code Formatting

```bash
# Check formatting with black
black --check md_simulation.py tests/

# Auto-fix formatting
black md_simulation.py tests/

# Check import sorting
isort --check-only md_simulation.py tests/

# Auto-fix imports
isort md_simulation.py tests/

# Check with flake8
flake8 md_simulation.py tests/ --max-line-length=100
```

### Git Workflow

```bash
# Check status
git status

# Add changes
git add .

# Commit with message
git commit -m "Your commit message"

# Push to trigger CI/CD
git push origin main

# Create and push new branch
git checkout -b feature/new-feature
git push origin feature/new-feature
```

## 📊 GitHub Actions

### View Workflow Runs

1. Go to repository on GitHub
2. Click **Actions** tab
3. Select workflow run to view details
4. Click job to see logs

### Manual Workflow Trigger

1. Go to **Actions** tab
2. Select workflow (e.g., "Tests")
3. Click **Run workflow** button
4. Select branch
5. Click **Run workflow**

### Download Artifacts

1. Go to workflow run summary
2. Scroll to **Artifacts** section
3. Click artifact name to download (e.g., coverage-report)

## 🔧 Workflow Files

### Location
```
.github/workflows/
├── tests.yml           # Comprehensive tests
└── tests-simple.yml    # Simple tests
```

### Edit Workflow

```bash
# Open in editor
code .github/workflows/tests.yml

# After editing, commit and push
git add .github/workflows/tests.yml
git commit -m "Update workflow configuration"
git push
```

## 🎯 Common Workflow Modifications

### Change Python Versions

Edit `tests.yml`:
```yaml
matrix:
  python-version: ['3.10', '3.11', '3.12']
```

### Change OS

Edit `tests.yml`:
```yaml
matrix:
  os: [ubuntu-latest, windows-latest]
```

### Change Trigger Branches

Edit workflow file:
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
```

### Add Environment Variables

```yaml
env:
  MY_VAR: value

jobs:
  test:
    env:
      JOB_VAR: value
    steps:
      - name: Step with env
        env:
          STEP_VAR: value
        run: echo $MY_VAR
```

## 🐛 Troubleshooting

### Workflow Not Running

```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/tests.yml'))"

# Or use online validator: https://www.yamllint.com/
```

### Tests Fail on CI But Pass Locally

```bash
# Test with specific Python version
python3.9 -m pytest tests/
python3.12 -m pytest tests/

# Test on different OS (use Docker)
docker run -it python:3.11 bash
# Then clone repo and run tests
```

### View Workflow Logs

```bash
# Install GitHub CLI
gh auth login

# View workflow runs
gh run list

# View specific run
gh run view RUN_ID

# View logs
gh run view RUN_ID --log
```

## 📝 Workflow Status

### Check Status via API

```bash
# Get latest workflow run status
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/YOUR_USERNAME/two_particles_MD/actions/runs
```

### Check Status via CLI

```bash
# Install GitHub CLI
gh auth login

# List recent runs
gh run list --workflow=tests.yml

# Watch run in real-time
gh run watch
```

## 🔐 Secrets Management

### Add Secret

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Enter name and value
4. Click **Add secret**

### Use Secret in Workflow

```yaml
steps:
  - name: Use secret
    env:
      MY_SECRET: ${{ secrets.MY_SECRET }}
    run: echo "Secret is set"
```

## 📦 Caching

### Cache pip packages (already in workflows)

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'  # Caches pip packages
```

### Custom cache

```yaml
- name: Cache custom directory
  uses: actions/cache@v3
  with:
    path: ~/.my_cache
    key: ${{ runner.os }}-cache-${{ hashFiles('**/requirements.txt') }}
```

## 🎨 Badge URLs

### Workflow Status Badge
```
https://github.com/YOUR_USERNAME/two_particles_MD/actions/workflows/tests.yml/badge.svg
```

### Specific Branch
```
https://github.com/YOUR_USERNAME/two_particles_MD/actions/workflows/tests.yml/badge.svg?branch=main
```

### Custom Badge (shields.io)
```
https://img.shields.io/badge/LABEL-MESSAGE-COLOR
```

## 📊 Coverage

### Generate HTML Report Locally

```bash
pytest tests/ --cov=md_simulation --cov-report=html
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

### Coverage Thresholds

Add to `pytest.ini` or `pyproject.toml`:
```ini
[tool:pytest]
addopts = --cov=md_simulation --cov-fail-under=80
```

## 🔄 Workflow Dispatch (Manual Trigger)

### Add to Workflow

```yaml
on:
  workflow_dispatch:
    inputs:
      debug:
        description: 'Enable debug mode'
        required: false
        default: 'false'
```

### Trigger via CLI

```bash
gh workflow run tests.yml
```

## 📚 Useful Links

- **Actions Tab**: `https://github.com/YOUR_USERNAME/two_particles_MD/actions`
- **Workflow File**: `https://github.com/YOUR_USERNAME/two_particles_MD/blob/main/.github/workflows/tests.yml`
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Workflow Syntax**: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions

## 💡 Tips

1. **Test locally first**: Always run tests locally before pushing
2. **Use draft PRs**: Create draft pull requests to test CI without notifying reviewers
3. **Check logs**: Always check workflow logs when tests fail
4. **Use caching**: Speed up workflows with dependency caching
5. **Fail fast**: Use `fail-fast: false` to see all failures, not just the first
6. **Matrix strategy**: Test multiple configurations efficiently
7. **Secrets**: Never commit secrets; use GitHub Secrets
8. **Branch protection**: Require passing tests before merging

## 🎯 Checklist Before Push

- [ ] Run tests locally: `pytest tests/ -v`
- [ ] Check coverage: `pytest tests/ --cov=md_simulation`
- [ ] Format code: `black md_simulation.py tests/`
- [ ] Sort imports: `isort md_simulation.py tests/`
- [ ] Check linting: `flake8 md_simulation.py tests/`
- [ ] Review changes: `git diff`
- [ ] Commit with clear message
- [ ] Push and monitor CI/CD

## 🚨 Emergency: Cancel Running Workflow

### Via GitHub UI
1. Go to **Actions** tab
2. Click on running workflow
3. Click **Cancel workflow** button

### Via CLI
```bash
gh run cancel RUN_ID
```

