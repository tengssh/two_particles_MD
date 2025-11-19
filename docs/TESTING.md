# Testing Guide

## ✅ Conversion Complete: unittest → pytest

The test suite has been successfully converted from `unittest` to `pytest`!

## 🎯 Why pytest?

### Advantages over unittest:

1. **Simpler syntax** - No need to inherit from `TestCase` or use `self.assert*`
2. **Better output** - More readable failure messages showing actual vs expected values
3. **Fixtures** - More powerful and flexible setup/teardown with `@pytest.fixture`
4. **Parametrization** - Easy to run same test with different inputs
5. **Less boilerplate** - Just write functions, not classes
6. **Better assertion introspection** - Automatically shows values in failures

### Example Comparison:

**unittest (old):**
```python
class TestParticle(unittest.TestCase):
    def setUp(self):
        self.position = np.array([1.0, 2.0])
        
    def test_kinetic_energy(self):
        particle = Particle(position=self.position, ...)
        self.assertAlmostEqual(particle.kinetic_energy, expected, places=5)
```

**pytest (new):**
```python
@pytest.fixture
def particle_params():
    return {'position': np.array([1.0, 2.0])}

def test_kinetic_energy(particle_params):
    particle = Particle(position=particle_params['position'], ...)
    assert particle.kinetic_energy == pytest.approx(expected, rel=1e-5)
```

## 📦 Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

Or install pytest directly:
```bash
pip install pytest pytest-cov
```

## 🚀 Running Tests

### Basic commands:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_particle.py

# Run specific test function
pytest tests/test_particle.py::test_kinetic_energy_moving_particle
```

### Advanced commands:

```bash
# Run with coverage report
pytest tests/ --cov=md_simulation --cov-report=term

# Generate HTML coverage report
pytest tests/ --cov=md_simulation --cov-report=html

# Run with detailed output
pytest tests/ -vv

# Show print statements
pytest tests/ -s

# Run only failed tests from last run
pytest tests/ --lf

# Stop at first failure
pytest tests/ -x
```

## 📊 Test Results

All 32 tests pass successfully:

```
=============================== test session starts ===============================
collected 32 items

tests/test_particle.py ........                                              [ 25%]
tests/test_potential.py ...............                                      [ 71%]
tests/test_simulation.py .........                                           [100%]

=============================== 32 passed in 0.78s ================================
```

### Coverage:
- **55% code coverage** - Tests cover core functionality
- Main simulation code: 250 statements, 138 covered

## 📝 Test Structure

### Fixtures Used:

**`test_particle.py`:**
- `particle_params` - Common particle parameters (position, velocity, mass)

**`test_potential.py`:**
- `lj_potential` - LennardJonesPotential instance with Argon parameters
- `lj_params` - Dictionary of Lennard-Jones parameters

**`test_simulation.py`:**
- `lj_potential` - Lennard-Jones potential for simulations
- `particles` - Tuple of two particles (one moving, one fixed)
- `simulation` - Complete TwoParticleMD simulation instance

### Test Coverage:

**Particle Tests (8 tests):**
- ✅ Initialization
- ✅ Kinetic energy (moving, fixed, stationary)
- ✅ Property mutability

**Potential Tests (15 tests):**
- ✅ Initialization
- ✅ Potential energy at various distances
- ✅ Force magnitude and direction
- ✅ Repulsive vs attractive regimes
- ✅ 2D force vectors

**Simulation Tests (9 tests):**
- ✅ Initialization
- ✅ Energy calculation and conservation
- ✅ Time stepping
- ✅ Wall collisions
- ✅ Fixed particle behavior
- ✅ History recording

## 🔧 Adding New Tests

Create a new test file or add to existing ones:

```python
import pytest
import numpy as np
from md_simulation import Particle

@pytest.fixture
def my_fixture():
    """Fixture providing test data."""
    return {'value': 42}

def test_something(my_fixture):
    """Test description."""
    result = calculate_something(my_fixture['value'])
    assert result == expected_value

def test_with_approx():
    """Test floating point comparison."""
    result = 3.14159265
    assert result == pytest.approx(3.14159, rel=1e-5)

def test_array_comparison():
    """Test numpy array comparison."""
    result = np.array([1.0, 2.0, 3.0])
    expected = np.array([1.0, 2.0, 3.0])
    np.testing.assert_array_equal(result, expected)
```

## 🎓 Pytest Features

### Parametrization:
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### Markers:
```python
@pytest.mark.slow
def test_long_running():
    # Long test
    pass

# Run only slow tests: pytest -m slow
# Skip slow tests: pytest -m "not slow"
```

### Exception testing:
```python
def test_raises_error():
    with pytest.raises(ValueError):
        raise ValueError("Expected error")
```

## 📚 Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)

## 🎉 Summary

✅ All tests converted from unittest to pytest  
✅ All 32 tests passing  
✅ 55% code coverage  
✅ Cleaner, more readable test code  
✅ Better error messages  
✅ Fixtures for reusable test setup  
✅ Coverage reporting enabled  

