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
pytest tests/ --cov=src --cov-report=term --cov-report=html
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
black src/ tests/

# Fix import sorting with isort
isort src/ tests/

# Check flake8 issues
flake8 src/ tests/ --max-line-length=100
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

---

## 🔧 CI Test Failures & Fixes (Historical Reference)

This section documents CI test failures encountered and their solutions for future reference.

### Issue 1: Streamlit Test Timeouts (Linux CI)

**Date:** 2024-11-27  
**Affected Tests:**
- `test_run_button_click`
- `test_simulation_produces_results`
- `test_session_state_stores_simulation`

**Error:**
```
RuntimeError: AppTest script run timed out after 3(s)
```

**Root Cause:**  
The Streamlit AppTest framework has a default 3-second timeout. Running MD simulations with 100 steps exceeded this timeout in CI environments.

**Solution:**  
Modified `tests/test_streamlit_app.py`:
1. Reduced simulation steps from 100 to 10
2. Increased timeout to 10 seconds

```python
# Before
at.number_input[5].set_value(100).run()
at.button[0].click().run()

# After
at.number_input[5].set_value(10).run()  # Minimal steps for fast test
at.button[0].click().run(timeout=10)    # Increased timeout
```

**Commit:** `94a1e59`

---

### Issue 2: macOS CI Crash

**Date:** 2024-11-27  
**Platform:** macOS runners  

**Error:**
```
Abort trap: 6
```

**Root Cause:**  
Matplotlib attempted to use an interactive backend (e.g., TkAgg, Qt5Agg) in a headless CI environment without a display server, causing a segmentation fault.

**Solution:**  
Added `MPLBACKEND=Agg` environment variable to force matplotlib to use the non-interactive Agg backend.

Modified `.github/workflows/tests.yml`:
```yaml
- name: Run tests with pytest
  env:
    MPLBACKEND: Agg  # Force non-interactive backend
  run: |
    pytest tests/ -v --tb=short

- name: Run tests with coverage
  env:
    MPLBACKEND: Agg  # Force non-interactive backend
  run: |
    pytest tests/ --cov=src --cov-report=xml --cov-report=term
```

**Commit:** `bf367c7`

---

### Issue 3: Windows CI Crash

**Date:** 2024-11-27  
**Platform:** Windows runners  

**Error:**
```
Windows fatal exception: code 0x80000003
```

**Stack Trace:**  
Crash occurred during pytest teardown phase after `test_simulation_produces_results`, indicating improper cleanup of matplotlib figures.

**Root Cause:**  
Matplotlib figures were not being properly closed after tests, causing memory/resource issues during teardown on Windows.

**Solution:**  
Modified `tests/test_streamlit_app.py`:

1. Set Agg backend at module level (before any matplotlib imports):
```python
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for CI
import matplotlib.pyplot as plt
```

2. Added pytest fixture for automatic cleanup:
```python
@pytest.fixture(autouse=True)
def cleanup_matplotlib():
    """Ensure all matplotlib figures are closed after each test."""
    yield
    plt.close('all')
```

**Why Both Changes?**
- `matplotlib.use('Agg')`: Prevents interactive backend issues
- `plt.close('all')`: Ensures proper cleanup even if tests create figures

**Commit:** `e99c813`

---

### Summary of Fixes

| Issue | Platform | Solution | Files Modified |
|-------|----------|----------|----------------|
| Test Timeout | Linux | Reduce steps, increase timeout | `tests/test_streamlit_app.py` |
| Abort Trap | macOS | Set `MPLBACKEND=Agg` env var | `.github/workflows/tests.yml` |
| Fatal Exception | Windows | Agg backend + cleanup fixture | `tests/test_streamlit_app.py` |

### Key Takeaways

1. **Always use non-interactive backends in CI**: Set `MPLBACKEND=Agg` or `matplotlib.use('Agg')`
2. **Clean up resources**: Use pytest fixtures with `autouse=True` for automatic cleanup
3. **Adjust timeouts for CI**: CI environments are slower than local machines
4. **Test locally on multiple platforms**: Use VMs or containers to catch platform-specific issues
5. **Keep test data minimal**: Use the smallest dataset that validates functionality

### Testing Matplotlib in CI

For any project using matplotlib in CI, add these safeguards:

**In workflow file:**
```yaml
env:
  MPLBACKEND: Agg
```

**In test file:**
```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

@pytest.fixture(autouse=True)
def cleanup_matplotlib():
    yield
    plt.close('all')
```

---

## 💡 Tips & Troubleshooting

### Git Authentication Issues

**Problem:** `remote rejected` error when pushing workflows

**Solution:** Use SSH instead of HTTPS for authentication

```bash
# Check current remote URL
git remote -v

# If using HTTPS (https://github.com/...)
origin  https://github.com/username/repo.git (fetch)
origin  https://github.com/username/repo.git (push)

# Switch to SSH (git@github.com:...)
git remote set-url origin git@github.com:username/repo.git

# Verify the change
git remote -v
origin  git@github.com:username/repo.git (fetch)
origin  git@github.com:username/repo.git (push)

# Now push works without OAuth scope issues
git push origin main
```

**Why?** GitHub requires the `workflow` scope for OAuth tokens when modifying files in `.github/workflows/`. SSH authentication bypasses this requirement.

### Windows Shell Commands

If you're on Windows, here's how to switch between different shells:

#### From PowerShell or CMD → Git Bash
```bash
# Launch Git Bash
"C:\Program Files\Git\bin\bash.exe"

# Or just click Git Bash icon in Start menu
```

#### From Git Bash → PowerShell
```bash
powershell
```

#### From Git Bash → CMD
```bash
cmd
```

#### From PowerShell → CMD
```powershell
cmd
```

#### From CMD → PowerShell
```cmd
powershell
```

#### Identifying Your Current Shell

**Git Bash (MINGW64):**
```bash
user@COMPUTER MINGW64 /d/project/repo (main)
$
```

**PowerShell:**
```powershell
PS D:\project\repo>
```

**CMD:**
```cmd
D:\project\repo>
```

### Common Workflow Issues

#### Workflow Not Triggering
- Check that workflow file is in `.github/workflows/`
- Verify YAML syntax (use a YAML validator)
- Ensure you pushed to the correct branch
- Check repository settings → Actions → Allow all actions

#### Tests Failing on CI but Passing Locally
- Check Python version differences
- Verify all dependencies in `requirements.txt`
- Check for OS-specific issues (paths, line endings)
- Review workflow logs for detailed error messages

#### Badge Not Updating
- Wait a few minutes for cache to clear
- Hard refresh browser (Ctrl+F5)
- Verify badge URL matches your username/repo
- Check that workflow has run at least once

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [Codecov Documentation](https://docs.codecov.com/)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Git SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

*Last Updated: 2024-11-27*
