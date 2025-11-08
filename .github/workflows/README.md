# GitHub Actions Workflows

This directory contains GitHub Actions workflows for automated testing and code quality checks.

## Available Workflows

### 1. `tests.yml` - Comprehensive Test Suite

**Triggers:**
- Push to `main`, `master`, or `develop` branches
- Pull requests to `main`, `master`, or `develop` branches
- Manual workflow dispatch

**Features:**
- ✅ **Multi-OS testing**: Ubuntu, Windows, macOS
- ✅ **Multi-Python version**: 3.9, 3.10, 3.11, 3.12
- ✅ **Test execution**: Runs all pytest tests with verbose output
- ✅ **Coverage reporting**: Generates coverage reports and uploads to Codecov
- ✅ **Code linting**: Checks code quality with flake8, black, and isort

**Matrix Strategy:**
- Tests run on 3 operating systems × 4 Python versions = 12 test jobs
- Continues even if one job fails (`fail-fast: false`)

**Linting Checks:**
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Code style and syntax errors

### 2. `tests-simple.yml` - Simple Test Suite

**Triggers:**
- Push to `main` or `master` branches
- Pull requests to `main` or `master` branches

**Features:**
- ✅ **Single environment**: Ubuntu with Python 3.11
- ✅ **Fast execution**: Quick feedback for basic testing
- ✅ **Coverage report**: Generates HTML coverage report
- ✅ **Artifact upload**: Coverage report available for download

**Use case:** Lightweight testing for quick validation

## Workflow Status Badges

Add these badges to your `README.md` to show workflow status:

### For `tests.yml`:
```markdown
![Tests](https://github.com/YOUR_USERNAME/two_particles_MD/actions/workflows/tests.yml/badge.svg)
```

### For `tests-simple.yml`:
```markdown
![Tests](https://github.com/YOUR_USERNAME/two_particles_MD/actions/workflows/tests-simple.yml/badge.svg)
```

### For Codecov (if configured):
```markdown
[![codecov](https://codecov.io/gh/YOUR_USERNAME/two_particles_MD/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/two_particles_MD)
```

## Setup Instructions

### 1. Enable GitHub Actions

GitHub Actions are automatically enabled for public repositories. For private repositories:
1. Go to repository **Settings** → **Actions** → **General**
2. Enable "Allow all actions and reusable workflows"

### 2. Configure Codecov (Optional)

For coverage reporting with `tests.yml`:

1. Sign up at [codecov.io](https://codecov.io) with your GitHub account
2. Add your repository to Codecov
3. Get your Codecov token
4. Add it as a repository secret:
   - Go to **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `CODECOV_TOKEN`
   - Value: Your Codecov token

### 3. Customize Workflows

Edit the workflow files to match your needs:

**Change trigger branches:**
```yaml
on:
  push:
    branches: [ main, develop, feature/* ]  # Add your branches
```

**Change Python versions:**
```yaml
matrix:
  python-version: ['3.9', '3.10', '3.11']  # Remove or add versions
```

**Change operating systems:**
```yaml
matrix:
  os: [ubuntu-latest, windows-latest]  # Remove macOS if not needed
```

## Viewing Test Results

### On GitHub:

1. Go to the **Actions** tab in your repository
2. Click on a workflow run to see details
3. Click on individual jobs to see logs
4. Download artifacts (coverage reports) from the workflow summary

### Locally:

Run the same commands that GitHub Actions uses:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=md_simulation --cov-report=term --cov-report=html
```

## Troubleshooting

### Tests fail on Windows but pass on Linux/macOS

- Check for path separator issues (`/` vs `\`)
- Use `os.path.join()` for cross-platform paths
- Check line ending differences (CRLF vs LF)

### Tests fail on specific Python version

- Check for version-specific syntax or features
- Review deprecation warnings
- Update dependencies in `requirements.txt`

### Linting failures

```bash
# Fix formatting with black
black md_simulation.py tests/

# Fix import sorting with isort
isort md_simulation.py tests/

# Check flake8 issues
flake8 md_simulation.py tests/ --max-line-length=100
```

## Best Practices

1. **Keep workflows fast**: Use caching for dependencies
2. **Test on multiple platforms**: Catch platform-specific bugs early
3. **Use matrix strategy**: Test multiple Python versions efficiently
4. **Monitor coverage**: Aim for >80% code coverage
5. **Fix linting issues**: Maintain consistent code style
6. **Review failed runs**: Don't ignore CI failures

## Workflow Files Structure

```
.github/
└── workflows/
    ├── README.md           # This file
    ├── tests.yml           # Comprehensive test suite
    └── tests-simple.yml    # Simple test suite
```

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [Codecov Documentation](https://docs.codecov.com/)
- [Python Package CI/CD Guide](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)

## Example Workflow Run

When you push code, GitHub Actions will:

1. ✅ Checkout your code
2. ✅ Set up Python environment
3. ✅ Install dependencies from `requirements.txt`
4. ✅ Run all tests with pytest
5. ✅ Generate coverage report
6. ✅ Upload coverage to Codecov (if configured)
7. ✅ Run linting checks (tests.yml only)
8. ✅ Report results with ✅ or ❌

You'll receive email notifications for failed runs (configurable in GitHub settings).

