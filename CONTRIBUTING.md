# Contributing to Two-Particle MD Simulation

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/two_particles_MD.git
cd two_particles_MD

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/two_particles_MD.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install black isort flake8
```

### 3. Create a Branch

```bash
# Create a new branch for your feature or fix
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Development Workflow

### 1. Make Your Changes

- Write clear, readable code
- Follow existing code style
- Add comments for complex logic
- Update documentation as needed

### 2. Write Tests

All new features and bug fixes should include tests:

```python
# tests/test_your_feature.py
import pytest
from md_simulation import YourClass

@pytest.fixture
def your_fixture():
    """Fixture for test setup."""
    return YourClass(param=value)

def test_your_feature(your_fixture):
    """Test that your feature works correctly."""
    result = your_fixture.method()
    assert result == expected_value
```

### 3. Run Tests Locally

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=md_simulation --cov-report=term

# Run specific test file
pytest tests/test_your_feature.py -v
```

### 4. Format Your Code

```bash
# Format with black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Check with flake8
flake8 src/ tests/ --max-line-length=100
```

### 5. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a clear message
git commit -m "Add feature: brief description"
```

**Commit Message Guidelines:**
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests when relevant

Examples:
```
Add temperature control feature
Fix wall collision bug for fixed particles
Update documentation for LJ potential
Refactor energy calculation method
```

### 6. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Go to GitHub and create a Pull Request
```

## 🧪 Testing Guidelines

### Test Requirements

- All new features must include tests
- Bug fixes should include regression tests
- Aim for >80% code coverage
- Tests should be fast and independent

### Test Structure

```python
# Good test structure
def test_specific_behavior():
    """Test description explaining what is being tested."""
    # Arrange: Set up test data
    particle = Particle(position=[1.0, 2.0], velocity=[0.1, 0.2])
    
    # Act: Perform the action
    result = particle.kinetic_energy
    
    # Assert: Check the result
    assert result == pytest.approx(expected_value, rel=1e-5)
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test
pytest tests/test_particle.py::test_kinetic_energy_moving_particle

# Stop at first failure
pytest tests/ -x

# Run only failed tests from last run
pytest tests/ --lf

# Show print statements
pytest tests/ -s
```

## 📚 Documentation Guidelines

### Code Documentation

- Add docstrings to all classes and methods
- Use clear, descriptive variable names
- Comment complex algorithms
- Update README.md for new features

### Docstring Format

```python
def method_name(self, param1, param2):
    """
    Brief description of what the method does.
    
    Parameters
    ----------
    param1 : type
        Description of param1
    param2 : type
        Description of param2
    
    Returns
    -------
    type
        Description of return value
    
    Examples
    --------
    >>> obj.method_name(value1, value2)
    expected_result
    """
    pass
```

## 🎨 Code Style Guidelines

### Python Style

- Follow PEP 8 style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use meaningful variable names

### Formatting Tools

We use automated tools to maintain consistent style:

- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting

```bash
# Auto-format before committing
black src/ tests/
isort src/ tests/
flake8 src/ tests/ --max-line-length=100
```

### Import Order

1. Standard library imports
2. Third-party imports
3. Local application imports

```python
# Standard library
import os
import sys

# Third-party
import numpy as np
import matplotlib.pyplot as plt

# Local
from md_simulation import Particle
```

## 🔍 Code Review Process

### What to Expect

1. **Automated Checks**: CI/CD will run tests automatically
2. **Code Review**: Maintainers will review your code
3. **Feedback**: You may be asked to make changes
4. **Approval**: Once approved, your PR will be merged

### Review Checklist

Before requesting review, ensure:

- [ ] All tests pass locally
- [ ] Code is formatted (black, isort)
- [ ] No linting errors (flake8)
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] PR description explains changes

## 🐛 Reporting Bugs

### Before Reporting

1. Check existing issues
2. Try to reproduce with latest version
3. Gather relevant information

### Bug Report Should Include

- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages and tracebacks
- Minimal code example

Use the bug report template: `.github/ISSUE_TEMPLATE/bug_report.md`

## 💡 Suggesting Features

### Feature Request Should Include

- Clear description of the feature
- Use case and benefits
- Proposed implementation (if any)
- Examples of how it would be used

Use the feature request template: `.github/ISSUE_TEMPLATE/feature_request.md`

## 📋 Pull Request Guidelines

### PR Requirements

- [ ] Descriptive title and description
- [ ] All tests pass
- [ ] Code is formatted and linted
- [ ] Documentation is updated
- [ ] Commits are clean and logical
- [ ] No merge conflicts

### PR Description Should Include

- What changes were made
- Why the changes were made
- How to test the changes
- Related issues (if any)

Use the PR template: `.github/pull_request_template.md`

## 🎯 Areas for Contribution

### Good First Issues

- Documentation improvements
- Adding more tests
- Fixing typos
- Adding examples

### Feature Ideas

- Temperature control (thermostat)
- Different potentials (Morse, harmonic)
- N-body simulation
- Periodic boundary conditions
- Animation of particle motion
- Velocity distributions

### Performance Improvements

- Optimize force calculations
- Vectorize operations
- Profile and optimize bottlenecks

## 🤝 Community Guidelines

### Be Respectful

- Be welcoming to newcomers
- Be patient with questions
- Provide constructive feedback
- Respect different viewpoints

### Communication

- Use clear, concise language
- Provide context and examples
- Ask questions if unclear
- Thank contributors

## 📞 Getting Help

- **Issues**: Open an issue for bugs or questions
- **Discussions**: Use GitHub Discussions for general questions
- **Documentation**: Check README.md and other docs

## 🎉 Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes (for significant contributions)
- CONTRIBUTORS.md file (if created)

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to Two-Particle MD Simulation! 🚀

