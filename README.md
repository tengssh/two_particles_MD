# Two-Particle Molecular Dynamics Simulation in 2D Box

![Tests](https://github.com/YOUR_USERNAME/two_particles_MD/actions/workflows/tests.yml/badge.svg)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI-Assisted](https://img.shields.io/badge/AI--Assisted-Augment%20Agent-blueviolet.svg)](https://www.augmentcode.com/)
[![Built with Claude](https://img.shields.io/badge/Built%20with-Claude%20Sonnet%204.5-orange.svg)](https://www.anthropic.com/)

## Overview
This is an educational implementation of a simplified molecular dynamics (MD) simulation featuring:
- **Two moving particles** starting at random positions (based on random seed)
- **Same initial velocity** for both particles
- **Lennard-Jones potential** for particle interactions
- **Elastic wall collisions** to keep particles in the box
- **Comprehensive test suite** with pytest (32 tests, 55% coverage)
- **CI/CD pipeline** with GitHub Actions

## Class Structure

### 1. `Particle` Class
Represents a single particle in 2D space with:
- **Position**: `[x, y]` coordinates in Angstroms
- **Velocity**: `[vx, vy]` in Angstroms/femtosecond
- **Mass**: in atomic mass units (amu)
- **is_fixed**: Boolean flag to make particle immobile

### 2. `LennardJonesPotential` Class
Implements the Lennard-Jones 6-12 potential:
```
U(r) = 4*epsilon * [(sigma/r)^12 - (sigma/r)^6]
```
- **epsilon**: Depth of potential well (energy scale)
- **sigma**: Zero-crossing distance (length scale)
- Provides methods for potential energy and force calculations

### 3. `TwoParticleMD` Class
Main simulation engine that:
- Uses **Velocity Verlet algorithm** for time integration
- Handles **wall collisions** elastically for both particles
- Tracks **energy conservation**
- Records trajectory history for both particles
- Provides visualization methods showing both trajectories

Note:
- Uses `setattr` and `getattr` to handle wall collision counters internally

## Key Features

### Physics Implementation
1. **Velocity Verlet Integration**: Time-reversible, symplectic integrator with good energy conservation
2. **Lennard-Jones Forces**: Realistic atomic interactions with attractive and repulsive components
3. **Elastic Wall Collisions**: Velocity reversal at boundaries conserves kinetic energy
4. **Energy Monitoring**: Tracks kinetic, potential, and total energy to verify simulation accuracy

### Visualization
- `plot_trajectory()`: Shows both particle paths in 2D box with walls, start and end positions
- `plot_energy()`: Displays energy components and conservation over time
- `plot_distance()`: Plots inter-particle distance vs time

## Running the Simulation

```python
python md_simulation.py
```

This will:
1. Create a 20×20 Angstrom box
2. Generate random starting positions for both particles (using seed 42)
3. Give both particles the same initial velocity (0.02, 0.02) Å/fs
4. Simulate for 5000 time steps (5 picoseconds)
5. Generate three plots showing trajectories, energy, and distance

## Example Usage

```python
import numpy as np
from md_simulation import Particle, LennardJonesPotential, TwoParticleMD

# Set random seed for reproducibility
np.random.seed(42)

# Create Lennard-Jones potential (Argon parameters)
lj = LennardJonesPotential(epsilon=0.238, sigma=3.4)

# Generate random positions (ensuring minimum separation)
pos1 = np.array([7.99, 17.21])
pos2 = np.array([13.71, 11.58])

# Same initial velocity for both particles
initial_velocity = np.array([0.02, 0.02])

# Create particles
particle1 = Particle(
    position=pos1,
    velocity=initial_velocity.copy(),
    mass=39.948
)

particle2 = Particle(
    position=pos2,
    velocity=initial_velocity.copy(),
    mass=39.948
)

# Run simulation
sim = TwoParticleMD(particle1, particle2, lj, box_size=(20.0, 20.0), dt=1.0)
sim.run(n_steps=5000)

# Visualize
sim.plot_trajectory()  # Shows both particle paths
sim.plot_energy()
sim.plot_distance()
```

## Educational Highlights

### Comments explain:
- **Physics concepts**: Kinetic energy, potential energy, forces
- **Numerical methods**: Why Velocity Verlet is better than Euler
- **Algorithm details**: Step-by-step breakdown of integration
- **Energy conservation**: Why it matters and how to check it

### Key Observations
1. **Wall bounces**: Both particles' velocities reverse at boundaries
2. **Particle interaction**: Attraction at long range, repulsion at short range
3. **Energy conservation**: Total energy should remain nearly constant
4. **Trajectory comparison**: Both particles start with same velocity but follow different paths due to different positions and interactions
5. **Collision dynamics**: Particles may collide, scatter, or orbit each other

## Parameters

### Typical Values
- **Time step (dt)**: 0.1-1.0 fs (smaller = better energy conservation)
- **Argon mass**: 39.948 amu
- **Argon LJ parameters**: ε = 0.238 kcal/mol, σ = 3.4 Å
- **Box size**: 10-50 Å (depends on application)
- **Initial velocity**: 0.001-0.1 Å/fs (room temperature ≈ 0.01 Å/fs)

## Extending the Code

Possible enhancements:
1. Add temperature control (thermostat)
2. Implement different potentials (harmonic, Morse, etc.)
3. Add more particles (N-body simulation)
4. Include external forces (gravity, electric field)
5. Implement periodic boundary conditions instead of walls
6. Add animation of particle motion
7. Calculate and plot velocity distributions

## Testing

This project includes a comprehensive test suite using pytest:

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=md_simulation --cov-report=term
```

**Test Coverage:**
- ✅ 32 tests covering all major components
- ✅ 55% code coverage
- ✅ Tests for Particle, LennardJonesPotential, and TwoParticleMD classes

See [`tests/README.md`](tests/README.md) for detailed testing documentation.

## Continuous Integration

GitHub Actions workflows automatically run tests on every push and pull request:

- **`tests.yml`**: Comprehensive testing on multiple OS (Ubuntu, Windows, macOS) and Python versions (3.9-3.12)
- **`tests-simple.yml`**: Quick testing on Ubuntu with Python 3.11

See [`.github/workflows/README.md`](.github/workflows/README.md) for CI/CD documentation.

## Dependencies
- `numpy>=1.20.0`: Numerical computations
- `matplotlib>=3.3.0`: Visualization
- `pytest>=7.0.0`: Testing framework
- `pytest-cov>=3.0.0`: Coverage reporting

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
two_particles_MD/
├── md_simulation.py          # Main simulation code
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── USAGE.md                  # Quick start guide
├── TESTING.md                # Testing guide
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── README.md             # Test documentation
│   ├── test_particle.py      # Particle class tests
│   ├── test_potential.py     # Potential class tests
│   └── test_simulation.py    # Simulation class tests
└── .github/
    └── workflows/            # CI/CD workflows
        ├── README.md         # Workflow documentation
        ├── tests.yml         # Comprehensive test suite
        └── tests-simple.yml  # Simple test suite
```

## Acknowledgments

This project was developed with assistance from **Augment Agent**, an agentic coding AI assistant developed by Augment Code, based on the Claude Sonnet 4.5 model by Anthropic.

### Development Contributions

Augment Agent assisted with:
- 🏗️ **Architecture Design**: Educational class structure with comprehensive documentation
- 🧪 **Test Suite**: Complete pytest-based testing infrastructure (32 tests, 55% coverage)
- 🔄 **CI/CD Pipeline**: GitHub Actions workflows for multi-platform, multi-version testing
- 📚 **Documentation**: Comprehensive guides including README, TESTING, CONTRIBUTING, and deployment checklists
- 🎨 **Visualization**: Matplotlib-based trajectory and energy plotting with customized styling
- 🔧 **Code Quality**: Integration of black, isort, and flake8 for maintaining code standards

### AI-Assisted Development

This project demonstrates the capabilities of AI-assisted software development, including:
- Rapid prototyping of scientific computing code
- Automated test generation and conversion (unittest → pytest)
- Professional CI/CD setup with multi-platform testing matrices
- Comprehensive documentation generation
- Best practices implementation for Python projects

**Model Information:**
- **AI Assistant**: Augment Agent
- **Developer**: Augment Code
- **Base Model**: Claude Sonnet 4.5 by Anthropic
- **Capabilities**: Codebase-aware context engine, multi-file editing, testing infrastructure, CI/CD setup

---

## License

MIT License - See LICENSE file for details

## Performance & Parallelization

While the current 2-particle system is already very fast, this project can be extended to N-body simulations with various parallelization techniques:

- 📊 **[PARALLELIZATION_GUIDE.md](PARALLELIZATION_GUIDE.md)** - Comprehensive guide to parallelization strategies
- 💻 **[examples/parallel_examples.py](examples/parallel_examples.py)** - Runnable benchmarks and code examples

### Parallelization Techniques Covered:
- **NumPy Vectorization** - 10-100x speedup, easy to implement
- **Numba JIT Compilation** - 10-100x speedup for complex loops
- **GPU Acceleration** - 50-500x speedup for large systems (PyTorch/CuPy)
- **Spatial Decomposition** - O(N²) → O(N) scaling for force calculations
- **MPI (Distributed Computing)** - 10-1000x speedup on HPC clusters
- **Ensemble Parallelism** - Perfect scaling for parameter studies
- **Async I/O** - Non-blocking data operations

See the guides for detailed explanations, code examples, and benchmarks!

---

## Branches

This repository maintains the following branches:
- **main**: The stable production branch containing the core implementation
- **research**: Active development branch for exploring new features and improvements

### Development Workflow
1. The `main` branch contains the stable, production-ready code
2. New features and research are developed in the `research` branch
3. Tested and validated improvements are merged back to `main` via pull requests

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

