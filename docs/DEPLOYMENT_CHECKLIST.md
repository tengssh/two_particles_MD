# Deployment Checklist

Use this checklist to deploy your project to GitHub with full CI/CD support.

## ✅ Pre-Deployment Checklist

### Local Testing

- [ ] All tests pass locally
  ```bash
  pytest tests/ -v
  ```

- [ ] Coverage is acceptable (currently 55%)
  ```bash
  pytest tests/ --cov=src --cov-report=term
  ```

- [ ] Code is formatted
  ```bash
  black src/ tests/
  ```

- [ ] Imports are sorted
  ```bash
  isort src/ tests/
  ```

- [ ] No linting errors
  ```bash
  flake8 src/ tests/ --max-line-length=100
  ```

- [ ] Simulation runs without errors
  ```bash
  python -m src.md_simulation
  ```

### Documentation Review

- [ ] README.md is complete and accurate
- [ ] docs/USAGE.md has correct examples
- [ ] docs/TESTING.md explains how to run tests
- [ ] docs/CONTRIBUTING.md has clear guidelines
- [ ] All code has docstrings

## 🚀 GitHub Deployment

### Step 1: Create GitHub Repository

- [ ] Go to [GitHub](https://github.com/new)
- [ ] Create new repository named `two_particles_MD`
- [ ] Choose public or private
- [ ] **Do NOT** initialize with README (we already have one)
- [ ] Click "Create repository"

### Step 2: Update README Badges

- [ ] Open `README.md`
- [ ] Replace `YOUR_USERNAME` with your GitHub username in badge URLs
  ```markdown
  ![Tests](https://github.com/YOUR_USERNAME/two_particles_MD/actions/workflows/tests.yml/badge.svg)
  ```

### Step 3: Initialize Git (if not already done)

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Two-particle MD simulation with CI/CD"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/two_particles_MD.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Verify GitHub Actions

- [ ] Go to repository on GitHub
- [ ] Click **Actions** tab
- [ ] Verify workflows are running
- [ ] Wait for all tests to complete
- [ ] Check that all jobs pass ✅

### Step 5: Review Workflow Results

- [ ] Click on workflow run
- [ ] Review each job (Ubuntu, Windows, macOS)
- [ ] Check test output
- [ ] Verify coverage reports
- [ ] Check linting results

## 🔧 Optional Configuration

### Codecov Setup (Optional)

- [ ] Sign up at [codecov.io](https://codecov.io)
- [ ] Connect GitHub account
- [ ] Add `two_particles_MD` repository
- [ ] Copy Codecov token
- [ ] Add token to GitHub Secrets:
  - Go to **Settings** → **Secrets and variables** → **Actions**
  - Click **New repository secret**
  - Name: `CODECOV_TOKEN`
  - Value: [paste token]
  - Click **Add secret**
- [ ] Update README with Codecov badge

### Branch Protection (Recommended)

- [ ] Go to **Settings** → **Branches**
- [ ] Click **Add rule**
- [ ] Branch name pattern: `main`
- [ ] Enable:
  - [ ] Require a pull request before merging
  - [ ] Require status checks to pass before merging
  - [ ] Require branches to be up to date before merging
  - [ ] Select status checks: `test (ubuntu-latest, 3.11)`
- [ ] Click **Create**

### GitHub Pages (Optional)

If you want to host coverage reports:

- [ ] Go to **Settings** → **Pages**
- [ ] Source: Deploy from a branch
- [ ] Branch: `gh-pages` (create if needed)
- [ ] Folder: `/root`
- [ ] Click **Save**

## 📝 Post-Deployment Tasks

### Verify Everything Works

- [ ] Clone repository in a new location
  ```bash
  git clone https://github.com/YOUR_USERNAME/two_particles_MD.git
  cd two_particles_MD
  ```

- [ ] Install dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Run tests
  ```bash
  pytest tests/ -v
  ```

- [ ] Run simulation
  ```bash
  python md_simulation.py
  ```

### Create First Release (Optional)

- [ ] Go to **Releases** → **Create a new release**
- [ ] Tag version: `v1.0.0`
- [ ] Release title: `v1.0.0 - Initial Release`
- [ ] Description:
  ```markdown
  ## Features
  - Two-particle molecular dynamics simulation
  - Lennard-Jones potential
  - Velocity Verlet integration
  - Comprehensive test suite (32 tests)
  - CI/CD with GitHub Actions
  
  ## Installation
  ```bash
  pip install -r requirements.txt
  ```
  
  ## Usage
  ```bash
  python md_simulation.py
  ```
  ```
- [ ] Click **Publish release**

### Share Your Project

- [ ] Add topics to repository:
  - Go to **About** (top right)
  - Add topics: `molecular-dynamics`, `physics`, `simulation`, `python`, `pytest`, `ci-cd`
  - Add description
  - Add website (if any)
  - Click **Save changes**

- [ ] Share on social media (optional)
- [ ] Add to your portfolio
- [ ] Link from your profile README

## 🧪 Testing the CI/CD Pipeline

### Test with a Pull Request

- [ ] Create a new branch
  ```bash
  git checkout -b test/ci-cd
  ```

- [ ] Make a small change (e.g., add comment)
  ```bash
  echo "# Test CI/CD" >> README.md
  ```

- [ ] Commit and push
  ```bash
  git add README.md
  git commit -m "Test: Verify CI/CD pipeline"
  git push origin test/ci-cd
  ```

- [ ] Create pull request on GitHub
- [ ] Verify CI/CD runs automatically
- [ ] Check all tests pass
- [ ] Merge or close PR

## 📊 Monitoring

### Regular Checks

- [ ] Monitor workflow runs weekly
- [ ] Review failed runs immediately
- [ ] Update dependencies monthly
- [ ] Check for security alerts
- [ ] Review and respond to issues

### Maintenance Tasks

- [ ] Update Python versions in workflows as needed
- [ ] Update dependencies in `requirements.txt`
- [ ] Add more tests to increase coverage
- [ ] Improve documentation based on feedback
- [ ] Review and merge dependabot PRs

## 🎯 Success Criteria

Your deployment is successful when:

- ✅ Repository is on GitHub
- ✅ All badges show "passing"
- ✅ CI/CD runs on every push
- ✅ Tests pass on all platforms
- ✅ Documentation is accessible
- ✅ Others can clone and run the project

## 🚨 Troubleshooting

### Workflows Not Running

**Problem:** Workflows don't appear in Actions tab

**Solutions:**
- [ ] Check `.github/workflows/` directory exists
- [ ] Verify YAML files are valid
- [ ] Check GitHub Actions are enabled in Settings
- [ ] Push a new commit to trigger workflows

### Tests Failing on CI

**Problem:** Tests pass locally but fail on CI

**Solutions:**
- [ ] Check Python version matches
- [ ] Verify all dependencies in `requirements.txt`
- [ ] Check for platform-specific issues
- [ ] Review workflow logs for details

### Badge Not Updating

**Problem:** Badge shows "no status" or wrong status

**Solutions:**
- [ ] Wait a few minutes for cache to clear
- [ ] Check workflow name matches badge URL
- [ ] Verify workflow has run at least once
- [ ] Hard refresh browser (Ctrl+F5)

## 📞 Getting Help

If you encounter issues:

1. **Check workflow logs** in Actions tab
2. **Review documentation** in this repository
3. **Search GitHub Actions docs**
4. **Open an issue** with details
5. **Check GitHub Status** page

## 🎉 Completion

Once all items are checked:

- ✅ Your project is deployed
- ✅ CI/CD is working
- ✅ Tests run automatically
- ✅ Documentation is complete
- ✅ Project is production-ready

**Congratulations! Your project is now live with professional CI/CD! 🚀**

---

## Quick Command Reference

```bash
# Local testing
pytest tests/ -v
pytest tests/ --cov=md_simulation

# Code formatting
black md_simulation.py tests/
isort md_simulation.py tests/
flake8 md_simulation.py tests/

# Git operations
git status
git add .
git commit -m "message"
git push origin main

# Create branch
git checkout -b feature/name
git push origin feature/name
```

## Important URLs

- Repository: `https://github.com/YOUR_USERNAME/two_particles_MD`
- Actions: `https://github.com/YOUR_USERNAME/two_particles_MD/actions`
- Settings: `https://github.com/YOUR_USERNAME/two_particles_MD/settings`
- Codecov: `https://codecov.io/gh/YOUR_USERNAME/two_particles_MD`

---

**Last Updated:** 2025-11-08  
**Version:** 1.0.0

