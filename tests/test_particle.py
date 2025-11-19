"""
Unit tests for the Particle class.
"""
import pytest
import numpy as np
import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.md_simulation import Particle


@pytest.fixture
def particle_params():
    """Fixture providing common particle parameters."""
    return {
        'position': np.array([1.0, 2.0]),
        'velocity': np.array([0.1, 0.2]),
        'mass': 39.948  # Argon mass
    }


def test_particle_initialization(particle_params):
    """Test that a particle is initialized correctly."""
    particle = Particle(
        position=particle_params['position'],
        velocity=particle_params['velocity'],
        mass=particle_params['mass']
    )

    np.testing.assert_array_equal(particle.position, particle_params['position'])
    np.testing.assert_array_equal(particle.velocity, particle_params['velocity'])
    assert particle.mass == particle_params['mass']
    assert particle.is_fixed is False
    np.testing.assert_array_equal(particle.force, np.zeros(2))


def test_fixed_particle(particle_params):
    """Test that a fixed particle is initialized correctly."""
    particle = Particle(
        position=particle_params['position'],
        velocity=particle_params['velocity'],
        mass=particle_params['mass'],
        is_fixed=True
    )

    assert particle.is_fixed is True


def test_kinetic_energy_moving_particle(particle_params):
    """Test kinetic energy calculation for a moving particle."""
    particle = Particle(
        position=particle_params['position'],
        velocity=particle_params['velocity'],
        mass=particle_params['mass']
    )

    # KE = 0.5 * m * v^2
    # v^2 = 0.1^2 + 0.2^2 = 0.01 + 0.04 = 0.05
    # KE = 0.5 * 39.948 * 0.05 = 0.99870
    expected_ke = 0.5 * particle_params['mass'] * np.dot(
        particle_params['velocity'], particle_params['velocity']
    )

    assert particle.kinetic_energy == pytest.approx(expected_ke, rel=1e-5)


def test_kinetic_energy_fixed_particle(particle_params):
    """Test that fixed particle has zero kinetic energy."""
    particle = Particle(
        position=particle_params['position'],
        velocity=particle_params['velocity'],
        mass=particle_params['mass'],
        is_fixed=True
    )

    assert particle.kinetic_energy == 0.0


def test_kinetic_energy_stationary_particle(particle_params):
    """Test kinetic energy of a stationary particle."""
    particle = Particle(
        position=particle_params['position'],
        velocity=np.array([0.0, 0.0]),
        mass=particle_params['mass']
    )

    assert particle.kinetic_energy == 0.0


def test_position_is_mutable(particle_params):
    """Test that particle position can be modified."""
    particle = Particle(
        position=particle_params['position'].copy(),
        velocity=particle_params['velocity'],
        mass=particle_params['mass']
    )

    new_position = np.array([5.0, 6.0])
    particle.position = new_position

    np.testing.assert_array_equal(particle.position, new_position)


def test_velocity_is_mutable(particle_params):
    """Test that particle velocity can be modified."""
    particle = Particle(
        position=particle_params['position'],
        velocity=particle_params['velocity'].copy(),
        mass=particle_params['mass']
    )

    new_velocity = np.array([0.5, 0.6])
    particle.velocity = new_velocity

    np.testing.assert_array_equal(particle.velocity, new_velocity)


def test_force_is_mutable(particle_params):
    """Test that particle force can be modified."""
    particle = Particle(
        position=particle_params['position'],
        velocity=particle_params['velocity'],
        mass=particle_params['mass']
    )

    new_force = np.array([1.0, 2.0])
    particle.force = new_force

    np.testing.assert_array_equal(particle.force, new_force)

