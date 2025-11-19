"""
Unit tests for the TwoParticleMD simulation class.
"""
import pytest
import numpy as np
import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.md_simulation import Particle, LennardJonesPotential, TwoParticleMD


@pytest.fixture
def lj_potential():
    """Fixture providing a Lennard-Jones potential."""
    epsilon = 0.238
    sigma = 3.4
    return LennardJonesPotential(epsilon=epsilon, sigma=sigma)


@pytest.fixture
def particles():
    """Fixture providing two particles for testing."""
    particle1 = Particle(
        position=np.array([5.0, 10.0]),
        velocity=np.array([0.01, 0.0]),
        mass=39.948
    )

    particle2 = Particle(
        position=np.array([15.0, 10.0]),
        velocity=np.array([0.0, 0.0]),
        mass=39.948,
        is_fixed=True
    )

    return particle1, particle2


@pytest.fixture
def simulation(particles, lj_potential):
    """Fixture providing a TwoParticleMD simulation."""
    particle1, particle2 = particles
    box_size = (20.0, 20.0)
    dt = 1.0

    return TwoParticleMD(
        particle1=particle1,
        particle2=particle2,
        potential=lj_potential,
        box_size=box_size,
        dt=dt
    )
    
def test_simulation_initialization(simulation):
    """Test that simulation is initialized correctly."""
    assert simulation.dt == 1.0
    assert simulation.time == 0.0
    assert simulation.box_size == (20.0, 20.0)
    assert simulation.wall_collision_count_1 == 0
    assert simulation.wall_collision_count_2 == 0


def test_energy_calculation(simulation):
    """Test that energy is calculated correctly."""
    ke, pe, total = simulation.get_energies()

    # Check that energies are finite
    assert np.isfinite(ke)
    assert np.isfinite(pe)
    assert np.isfinite(total)

    # Check energy conservation equation
    assert total == pytest.approx(ke + pe, rel=1e-10)


def test_single_step(simulation):
    """Test that a single simulation step executes without error."""
    initial_time = simulation.time
    simulation.step()

    # Time should advance by dt
    assert simulation.time == pytest.approx(initial_time + simulation.dt, rel=1e-10)


def test_run_simulation(simulation):
    """Test that simulation runs for specified number of steps."""
    n_steps = 100
    simulation.run(n_steps=n_steps, record_interval=10)

    # Check that time advanced correctly
    expected_time = n_steps * simulation.dt
    assert simulation.time == pytest.approx(expected_time, rel=1e-5)

    # Check that history was recorded
    assert len(simulation.history['time']) > 0
    assert len(simulation.history['pos1']) > 0
    assert len(simulation.history['pos2']) > 0
    
def test_wall_collision_left(lj_potential):
    """Test that particle bounces off left wall."""
    particle = Particle(
        position=np.array([0.5, 10.0]),
        velocity=np.array([-0.1, 0.0]),  # Moving left
        mass=39.948
    )

    fixed_particle = Particle(
        position=np.array([15.0, 10.0]),
        velocity=np.array([0.0, 0.0]),
        mass=39.948,
        is_fixed=True
    )

    sim = TwoParticleMD(
        particle1=particle,
        particle2=fixed_particle,
        potential=lj_potential,
        box_size=(20.0, 20.0),
        dt=10.0  # Large dt to ensure collision
    )

    initial_collisions = sim.wall_collision_count_1
    sim.step()

    # Particle should have bounced
    assert particle.velocity[0] > 0.0  # Velocity reversed
    assert sim.wall_collision_count_1 >= initial_collisions


def test_wall_collision_right(lj_potential):
    """Test that particle bounces off right wall."""
    particle = Particle(
        position=np.array([19.5, 10.0]),
        velocity=np.array([0.1, 0.0]),  # Moving right
        mass=39.948
    )

    fixed_particle = Particle(
        position=np.array([5.0, 10.0]),
        velocity=np.array([0.0, 0.0]),
        mass=39.948,
        is_fixed=True
    )

    sim = TwoParticleMD(
        particle1=particle,
        particle2=fixed_particle,
        potential=lj_potential,
        box_size=(20.0, 20.0),
        dt=10.0
    )

    sim.step()

    # Particle should have bounced
    assert particle.velocity[0] < 0.0  # Velocity reversed


def test_fixed_particle_does_not_move(simulation, particles):
    """Test that fixed particle stays in place."""
    _, particle2 = particles

    initial_pos = particle2.position.copy()
    simulation.run(n_steps=100, record_interval=1)

    # Fixed particle should not have moved
    np.testing.assert_array_equal(particle2.position, initial_pos)


def test_energy_conservation(lj_potential):
    """Test that energy is approximately conserved."""
    # Use smaller time step for better energy conservation
    particle1 = Particle(
        position=np.array([8.0, 10.0]),
        velocity=np.array([0.01, 0.0]),
        mass=39.948
    )

    particle2 = Particle(
        position=np.array([12.0, 10.0]),
        velocity=np.array([0.0, 0.0]),
        mass=39.948,
        is_fixed=True
    )

    sim = TwoParticleMD(
        particle1=particle1,
        particle2=particle2,
        potential=lj_potential,
        box_size=(20.0, 20.0),
        dt=0.1  # Small time step
    )

    initial_ke, initial_pe, initial_total = sim.get_energies()
    sim.run(n_steps=100, record_interval=1)
    final_ke, final_pe, final_total = sim.get_energies()

    # Energy drift should be small (< 5% for this test)
    energy_drift = abs(final_total - initial_total) / abs(initial_total)
    assert energy_drift < 0.05


def test_history_recording(simulation):
    """Test that simulation history is recorded correctly."""
    n_steps = 50
    record_interval = 5
    simulation.run(n_steps=n_steps, record_interval=record_interval)

    # Check that history has correct length
    expected_records = n_steps // record_interval + 1  # +1 for initial state
    assert len(simulation.history['time']) == expected_records
    assert len(simulation.history['pos1']) == expected_records
    assert len(simulation.history['kinetic']) == expected_records

