"""
Unit tests for the LennardJonesPotential class.
"""
import pytest
import numpy as np
import sys
import os

# Add parent directory to path to import md_simulation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from md_simulation import LennardJonesPotential


@pytest.fixture
def lj_potential():
    """Fixture providing a LennardJonesPotential instance with Argon parameters."""
    epsilon = 0.238  # kcal/mol (Argon)
    sigma = 3.4      # Angstrom (Argon)
    return LennardJonesPotential(epsilon=epsilon, sigma=sigma)


@pytest.fixture
def lj_params():
    """Fixture providing Lennard-Jones parameters."""
    return {
        'epsilon': 0.238,  # kcal/mol (Argon)
        'sigma': 3.4       # Angstrom (Argon)
    }


def test_initialization(lj_potential, lj_params):
    """Test that potential is initialized correctly."""
    assert lj_potential.epsilon == lj_params['epsilon']
    assert lj_potential.sigma == lj_params['sigma']
    
def test_potential_at_equilibrium(lj_potential, lj_params):
    """Test potential energy at equilibrium distance."""
    # Equilibrium distance: r_eq = 2^(1/6) * sigma
    r_eq = 2 ** (1/6) * lj_params['sigma']

    # At equilibrium, U(r_eq) = -epsilon
    potential = lj_potential.potential(r_eq)

    assert potential == pytest.approx(-lj_params['epsilon'], rel=1e-5)


def test_potential_at_sigma(lj_potential, lj_params):
    """Test potential energy at r = sigma (zero crossing)."""
    # At r = sigma, U(sigma) = 0
    potential = lj_potential.potential(lj_params['sigma'])

    assert potential == pytest.approx(0.0, abs=1e-10)


def test_potential_at_infinity(lj_potential, lj_params):
    """Test potential energy at large distance."""
    # At large r, U(r) -> 0
    potential = lj_potential.potential(100.0 * lj_params['sigma'])

    assert potential == pytest.approx(0.0, rel=1e-5)


def test_potential_is_repulsive_at_short_range(lj_potential, lj_params):
    """Test that potential is positive (repulsive) at short distances."""
    r_short = 0.9 * lj_params['sigma']
    potential = lj_potential.potential(r_short)

    assert potential > 0.0


def test_potential_is_attractive_at_medium_range(lj_potential, lj_params):
    """Test that potential is negative (attractive) at medium distances."""
    r_medium = 1.2 * lj_params['sigma']
    potential = lj_potential.potential(r_medium)

    assert potential < 0.0
    
def test_force_magnitude_at_equilibrium(lj_potential, lj_params):
    """Test that force is zero at equilibrium distance."""
    r_eq = 2 ** (1/6) * lj_params['sigma']
    force = lj_potential.force_magnitude(r_eq)

    assert force == pytest.approx(0.0, abs=1e-5)


def test_force_is_repulsive_at_short_range(lj_potential, lj_params):
    """Test that force is positive (repulsive) at short distances."""
    r_short = 0.9 * lj_params['sigma']
    force = lj_potential.force_magnitude(r_short)

    assert force > 0.0


def test_force_is_attractive_at_medium_range(lj_potential, lj_params):
    """Test that force is negative (attractive) at medium distances."""
    r_medium = 1.5 * lj_params['sigma']
    force = lj_potential.force_magnitude(r_medium)

    assert force < 0.0


def test_force_vector_direction(lj_potential, lj_params):
    """Test that force vector points in correct direction."""
    # At equilibrium distance, force should be zero
    r_eq = 2 ** (1/6) * lj_params['sigma']
    r_vector = np.array([r_eq, 0.0])
    force_vector = lj_potential.force_vector(r_vector)

    # At equilibrium, force should be zero
    np.testing.assert_array_almost_equal(force_vector, np.array([0.0, 0.0]), decimal=5)
    
def test_force_vector_repulsive(lj_potential, lj_params):
    """Test force vector in repulsive regime."""
    # Short distance: particles should repel
    r_vector = np.array([0.9 * lj_params['sigma'], 0.0])
    force_vector = lj_potential.force_vector(r_vector)

    # Force should point in same direction as r_vector (repulsive)
    assert force_vector[0] > 0.0
    assert force_vector[1] == pytest.approx(0.0, abs=1e-10)


def test_force_vector_attractive(lj_potential, lj_params):
    """Test force vector in attractive regime."""
    # Medium distance: particles should attract
    r_vector = np.array([1.5 * lj_params['sigma'], 0.0])
    force_vector = lj_potential.force_vector(r_vector)

    # Force should point opposite to r_vector (attractive)
    assert force_vector[0] < 0.0
    assert force_vector[1] == pytest.approx(0.0, abs=1e-10)


def test_force_vector_2d(lj_potential):
    """Test force vector in 2D."""
    r_vector = np.array([3.0, 4.0])  # Distance = 5.0
    force_vector = lj_potential.force_vector(r_vector)

    # Force should be parallel to r_vector
    # Check that force_vector = k * r_vector for some scalar k
    ratio = force_vector[0] / r_vector[0]
    assert force_vector[1] / r_vector[1] == pytest.approx(ratio, rel=1e-10)


def test_potential_decreases_with_distance(lj_potential, lj_params):
    """Test that potential magnitude decreases at large distances."""
    # At large distances, potential should approach zero
    r1 = 10.0 * lj_params['sigma']
    r2 = 20.0 * lj_params['sigma']

    potential1 = abs(lj_potential.potential(r1))
    potential2 = abs(lj_potential.potential(r2))

    # Potential should be smaller at larger distance
    assert potential2 < potential1


def test_force_decreases_with_distance(lj_potential, lj_params):
    """Test that force magnitude decreases at large distances."""
    # At large distances, force should approach zero
    r1 = 10.0 * lj_params['sigma']
    r2 = 20.0 * lj_params['sigma']

    force1 = abs(lj_potential.force_magnitude(r1))
    force2 = abs(lj_potential.force_magnitude(r2))

    # Force should be smaller at larger distance
    assert force2 < force1

