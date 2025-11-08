# Test Suite for Two-Particle MD Simulation

## Overview
This directory contains unit tests for the molecular dynamics simulation code using **pytest**.

## Installation

First, install the required dependencies:
```bash
pip install -r requirements.txt
```

Or install pytest directly:
```bash
pip install pytest pytest-cov
```

## Test Files

### `test_particle.py`
Tests for the `Particle` class:
- Initialization (position, velocity, mass, fixed status)
- Kinetic energy calculation
- Fixed vs moving particles
- Mutability of properties

### `test_potential.py`
Tests for the `LennardJonesPotential` class:
- Potential energy at various distances
- Force magnitude and direction
- Equilibrium distance behavior
- Repulsive vs attractive regimes
- Force decay with distance

### `test_simulation.py`
Tests for the `TwoParticleMD` simulation class:
- Simulation initialization
- Energy calculation and conservation
- Time stepping (single step and multiple steps)
- Wall collision detection and handling
- Fixed particle behavior
- History recording

## Running Tests

### Run all tests:
```bash
pytest tests/
```

### Run with verbose output:
```bash
pytest tests/ -v
```

### Run a specific test file:
```bash
pytest tests/test_particle.py
pytest tests/test_potential.py
pytest tests/test_simulation.py
```

### Run a specific test function:
```bash
pytest tests/test_particle.py::test_kinetic_energy_moving_particle
pytest tests/test_potential.py::test_force_vector_attractive
```

### Run with coverage report:
```bash
pytest tests/ --cov=md_simulation --cov-report=html
```

### Run with detailed output:
```bash
pytest tests/ -vv
```

### Run and show print statements:
```bash
pytest tests/ -s
```

## Test Coverage

The test suite covers:
- ✅ Particle initialization and properties
- ✅ Kinetic energy calculations
- ✅ Lennard-Jones potential and forces
- ✅ Force direction (attractive vs repulsive)
- ✅ Simulation time stepping
- ✅ Wall collision handling
- ✅ Energy conservation
- ✅ Fixed particle behavior
- ✅ History recording

## Expected Output

When all tests pass, you should see:
```
================================ test session starts =================================
collected 32 items

tests/test_particle.py ........                                              [ 25%]
tests/test_potential.py ...............                                      [ 71%]
tests/test_simulation.py .........                                           [100%]

================================= 32 passed in 0.15s =================================
```

## Adding New Tests

To add new tests:
1. Create a new test file in the `tests/` directory (e.g., `test_new_feature.py`)
2. Import necessary modules and the code to test
3. Write test functions starting with `test_`
4. Use pytest fixtures for setup/teardown
5. Use simple `assert` statements to verify expected behavior

Example:
```python
import pytest
from md_simulation import MyNewClass

@pytest.fixture
def my_object():
    """Fixture providing a test object."""
    return MyNewClass(param1=10, param2=20)

def test_something(my_object):
    """Test that something works correctly."""
    result = my_object.method()
    assert result == expected_value

def test_with_approx():
    """Test floating point values."""
    result = calculate_something()
    assert result == pytest.approx(3.14159, rel=1e-5)
```
Note:
- Add module path: `sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))`
- Useful pytest functions: `pytest.approx(test_value, rel=tolerance)`
- Useful numpy functions: `np.isfinite()`, `np.testing.assert_array_equal(array1, array2)`, `np.testing.assert_array_almost_equal(array1, array2, decimal=5)`

## Pytest Advantages

- **Simpler syntax**: No need for `self.assert*` methods
- **Better output**: More readable failure messages with actual values
- **Fixtures**: Powerful setup/teardown with `@pytest.fixture`
- **Parametrization**: Easy to test multiple inputs with `@pytest.mark.parametrize`
- **Less boilerplate**: Just write functions, not classes

## Continuous Integration

These tests can be integrated into CI/CD pipelines:
- GitHub Actions
- Travis CI
- Jenkins
- etc.

Example GitHub Actions workflow:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install numpy matplotlib
      - run: python -m unittest discover tests
```

