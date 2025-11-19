#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Two-Particle Molecular Dynamics Simulation

A simple 2D molecular dynamics simulation of two particles interacting
via the Lennard-Jones potential in a rectangular box with elastic walls.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional

# Fix encoding for Windows console (but not when running under pytest or in tests)
# This prevents UnicodeEncodeError on Windows with CP950/CP936 encoding
if sys.platform == 'win32' and 'pytest' not in sys.modules and 'unittest' not in sys.modules:
    import io
    # Only wrap if stdout/stderr have a buffer attribute (real console)
    if (hasattr(sys.stdout, 'buffer') and
        hasattr(sys.stderr, 'buffer') and
        not isinstance(sys.stdout, io.TextIOWrapper)):
        try:
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer,
                encoding='utf-8',
                errors='replace',
                line_buffering=True
            )
            sys.stderr = io.TextIOWrapper(
                sys.stderr.buffer,
                encoding='utf-8',
                errors='replace',
                line_buffering=True
            )
        except (AttributeError, ValueError, OSError):
            # If wrapping fails, just continue without encoding fix
            pass


class Particle:
    """
    Represents a single particle in the 2D molecular dynamics simulation.

    A particle has three fundamental properties:
    - Position: where it is in 2D space (x, y coordinates)
    - Velocity: how fast and in what direction it's moving
    - Mass: its inertia (resistance to acceleration)

    Attributes:
        position (np.ndarray): 2D position vector [x, y] in Angstroms
        velocity (np.ndarray): 2D velocity vector [vx, vy] in Angstroms/fs
        mass (float): Particle mass in atomic mass units (amu)
        force (np.ndarray): Current force acting on particle in kcal/(mol*Angstrom)
        is_fixed (bool): If True, particle doesn't move (fixed in space)
    """

    def __init__(self, position: np.ndarray, velocity: np.ndarray,
                 mass: float = 1.0, is_fixed: bool = False):
        """
        Initialize a particle with position, velocity, and mass.

        Args:
            position: 2D numpy array [x, y]
            velocity: 2D numpy array [vx, vy]
            mass: Particle mass (default: 1.0 amu)
            is_fixed: If True, particle is fixed in space (default: False)
        """
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass
        self.force = np.zeros(2)  # Force will be calculated during simulation
        self.is_fixed = is_fixed

    @property
    def kinetic_energy(self) -> float:
        """
        Calculate the kinetic energy of the particle.

        Kinetic energy: KE = (1/2) * m * v^2
        where v^2 is the squared magnitude of velocity vector

        Returns:
            Kinetic energy in kcal/mol
        """
        # Fixed particles have no kinetic energy
        if self.is_fixed:
            return 0.0
        # np.dot(v, v) gives v^2 = vx^2 + vy^2
        return 0.5 * self.mass * np.dot(self.velocity, self.velocity)

    def __repr__(self) -> str:
        """String representation for debugging."""
        fixed_str = " [FIXED]" if self.is_fixed else ""
        return f"Particle(pos={self.position}, vel={self.velocity}, mass={self.mass}){fixed_str}"


class LennardJonesPotential:
    """
    Implements the Lennard-Jones potential for particle interactions.

    The Lennard-Jones (LJ) potential is one of the most common models for
    describing interactions between neutral atoms or molecules. It has two parts:

    1. Attractive term (van der Waals): -C/r^6 (dominates at medium distances)
    2. Repulsive term (Pauli exclusion): +C/r^12 (dominates at short distances)

    Mathematical form:
        U(r) = 4*epsilon * [(sigma/r)^12 - (sigma/r)^6]

    Where:
        - epsilon: Depth of the potential well (energy scale)
        - sigma: Distance at which potential is zero (length scale)
        - r: Distance between particles

    The minimum of the potential occurs at r = 2^(1/6) * sigma ~= 1.122 * sigma

    Attributes:
        epsilon (float): Energy parameter in kcal/mol
        sigma (float): Length parameter in Angstroms
    """

    def __init__(self, epsilon: float = 1.0, sigma: float = 1.0):
        """
        Initialize Lennard-Jones potential parameters.

        Args:
            epsilon: Depth of potential well (default: 1.0 kcal/mol)
            sigma: Zero-crossing distance (default: 1.0 Angstrom)
        """
        self.epsilon = epsilon
        self.sigma = sigma

    def potential(self, r: float) -> float:
        """
        Calculate the Lennard-Jones potential energy at distance r.

        U(r) = 4*epsilon * [(sigma/r)^12 - (sigma/r)^6]

        Args:
            r: Distance between particles (scalar)

        Returns:
            Potential energy in kcal/mol
        """
        # Avoid division by zero
        if r < 1e-10:
            return np.inf

        # Calculate (sigma/r)^6 once to avoid redundant computation
        sr6 = (self.sigma / r) ** 6

        # LJ potential: repulsive term (sr6^2) minus attractive term (sr6)
        return 4.0 * self.epsilon * (sr6 ** 2 - sr6)

    def force_magnitude(self, r: float) -> float:
        """
        Calculate the magnitude of force at distance r.

        The force is the negative gradient of potential: F = -dU/dr

        For LJ potential:
            F(r) = 24*epsilon/r * [2*(sigma/r)^12 - (sigma/r)^6]

        Positive F means repulsive (push apart), negative means attractive (pull together)

        Args:
            r: Distance between particles

        Returns:
            Force magnitude (positive = repulsive, negative = attractive)
        """
        # Avoid division by zero
        if r < 1e-10:
            return 0.0  # At r=0, we cap the force to avoid infinities

        # Calculate (sigma/r)^6 once
        sr6 = (self.sigma / r) ** 6

        # Force magnitude from derivative of LJ potential
        # Factor of 24 comes from: d/dr[(sigma/r)^12] = -12*sigma^12/r^13
        return 24.0 * self.epsilon / r * (2.0 * sr6 ** 2 - sr6)

    def force_vector(self, r_vector: np.ndarray) -> np.ndarray:
        """
        Calculate the force vector between two particles.

        The force vector points from particle 2 to particle 1 (the direction
        particle 1 is pushed). It's calculated as:
            F_vector = F_magnitude * (r_vector / |r_vector|)

        where r_vector = position1 - position2

        Args:
            r_vector: Displacement vector from particle 2 to particle 1 (2D)

        Returns:
            Force vector acting on particle 1 (Newton's 3rd law: force on
            particle 2 is the negative of this)
        """
        # Calculate distance (magnitude of displacement vector)
        r = np.linalg.norm(r_vector)

        # Avoid division by zero
        if r < 1e-10:
            return np.zeros(2)  # 2D force vector

        # Unit vector pointing from particle 2 to particle 1
        r_hat = r_vector / r

        # Force vector = magnitude * direction
        return self.force_magnitude(r) * r_hat


class TwoParticleMD:
    """
    Molecular Dynamics simulation for two interacting particles in a 2D box.

    This class implements a complete MD simulation using the Velocity Verlet
    algorithm, which is a symplectic integrator that conserves energy well.

    Both particles move and interact with each other via Lennard-Jones potential.
    Both particles bounce off the walls of a 2D rectangular box.

    The Velocity Verlet algorithm updates positions and velocities as:
        1. Calculate forces at current positions
        2. Update positions: r(t+dt) = r(t) + v(t)*dt + 0.5*a(t)*dt^2
        3. Calculate forces at new positions
        4. Update velocities: v(t+dt) = v(t) + 0.5*[a(t) + a(t+dt)]*dt

    This algorithm is time-reversible and has better energy conservation
    than simpler methods like Euler integration.

    Attributes:
        particle1 (Particle): First particle
        particle2 (Particle): Second particle
        potential (LennardJonesPotential): Interaction potential
        dt (float): Time step in femtoseconds
        time (float): Current simulation time
        box_size (tuple): (width, height) of the 2D box in Angstroms
        history (dict): Stores trajectory and energy data
    """

    def __init__(self,
                 particle1: Particle,
                 particle2: Particle,
                 potential: LennardJonesPotential,
                 box_size: Tuple[float, float] = (20.0, 20.0),
                 dt: float = 0.001):
        """
        Initialize the two-particle MD simulation in a 2D box.

        Args:
            particle1: First particle
            particle2: Second particle
            potential: Interaction potential (e.g., Lennard-Jones)
            box_size: (width, height) of the 2D box (default: 20x20 Angstroms)
            dt: Time step in femtoseconds (default: 0.001 fs = 1 attosecond)
        """
        self.particle1 = particle1
        self.particle2 = particle2
        self.potential = potential
        self.dt = dt
        self.time = 0.0
        self.box_size = box_size

        # History storage for analysis and visualization
        # Each list will store values at each time step
        self.history = {
            'time': [],
            'pos1': [],        # Particle 1 positions
            'pos2': [],        # Particle 2 positions
            'vel1': [],        # Particle 1 velocities
            'vel2': [],        # Particle 2 velocities
            'kinetic': [],     # Kinetic energy
            'potential': [],   # Potential energy
            'total': [],       # Total energy (should be conserved!)
            'wall_collisions_1': [],  # Particle 1 wall collisions
            'wall_collisions_2': []   # Particle 2 wall collisions
        }

        self.wall_collision_count_1 = 0
        self.wall_collision_count_2 = 0

        # Calculate initial forces
        self._calculate_forces()

    def _calculate_forces(self) -> None:
        """
        Calculate forces on both particles based on their current positions.

        This is a private method (indicated by leading underscore) called
        internally during the simulation.

        Newton's 3rd Law: F_12 = -F_21
        If particle 1 feels force F from particle 2, then particle 2 feels -F
        """
        # Displacement vector from particle 2 to particle 1
        r_vector = self.particle1.position - self.particle2.position

        # Calculate force on particle 1
        force_on_1 = self.potential.force_vector(r_vector)

        # Apply Newton's 3rd law: force on particle 2 is opposite
        self.particle1.force = force_on_1
        self.particle2.force = -force_on_1

    def _handle_wall_collisions(self, particle, collision_counter_attr: str) -> None:
        """
        Handle elastic collisions with the box walls for a given particle.

        When a particle hits a wall, we reverse the appropriate
        velocity component (elastic collision). This conserves kinetic energy.

        Box boundaries: x in [0, box_width], y in [0, box_height]

        Args:
            particle: The particle to check for wall collisions
            collision_counter_attr: Name of the collision counter attribute
                                   ('wall_collision_count_1' or 'wall_collision_count_2')
        """
        # Skip if particle is fixed
        if particle.is_fixed:
            return

        pos = particle.position
        vel = particle.velocity
        width, height = self.box_size

        collision_occurred = False

        # Check left and right walls (x-direction)
        if pos[0] <= 0:
            pos[0] = 0
            vel[0] = abs(vel[0])  # Bounce right
            collision_occurred = True
        elif pos[0] >= width:
            pos[0] = width
            vel[0] = -abs(vel[0])  # Bounce left
            collision_occurred = True

        # Check bottom and top walls (y-direction)
        if pos[1] <= 0:
            pos[1] = 0
            vel[1] = abs(vel[1])  # Bounce up
            collision_occurred = True
        elif pos[1] >= height:
            pos[1] = height
            vel[1] = -abs(vel[1])  # Bounce down
            collision_occurred = True

        if collision_occurred:
            current_count = getattr(self, collision_counter_attr)
            setattr(self, collision_counter_attr, current_count + 1)

    def step(self) -> None:
        """
        Perform one time step of the simulation using Velocity Verlet algorithm.

        Velocity Verlet is a two-stage process:
        Stage 1: Update positions using current velocities and accelerations
        Stage 2: Update velocities using average of old and new accelerations

        After updating, we check for wall collisions and handle them.

        This method is the heart of the MD simulation!
        """
        # Store old accelerations (a = F/m from Newton's 2nd law)
        old_accel1 = self.particle1.force / self.particle1.mass
        old_accel2 = self.particle2.force / self.particle2.mass

        # Stage 1: Update positions
        # New position = old position + velocity*dt + 0.5*acceleration*dt^2
        if not self.particle1.is_fixed:
            self.particle1.position += (self.particle1.velocity * self.dt +
                                        0.5 * old_accel1 * self.dt ** 2)

        if not self.particle2.is_fixed:
            self.particle2.position += (self.particle2.velocity * self.dt +
                                        0.5 * old_accel2 * self.dt ** 2)

        # Handle wall collisions (elastic bounces) for both particles
        self._handle_wall_collisions(self.particle1, 'wall_collision_count_1')
        self._handle_wall_collisions(self.particle2, 'wall_collision_count_2')

        # Calculate forces at new positions
        self._calculate_forces()

        # New accelerations at updated positions
        new_accel1 = self.particle1.force / self.particle1.mass
        new_accel2 = self.particle2.force / self.particle2.mass

        # Stage 2: Update velocities using average acceleration
        # New velocity = old velocity + 0.5*(old acceleration + new acceleration)*dt
        if not self.particle1.is_fixed:
            self.particle1.velocity += 0.5 * (old_accel1 + new_accel1) * self.dt

        if not self.particle2.is_fixed:
            self.particle2.velocity += 0.5 * (old_accel2 + new_accel2) * self.dt

        # Increment simulation time
        self.time += self.dt

    def get_energies(self) -> Tuple[float, float, float]:
        """
        Calculate current kinetic, potential, and total energy.

        Energy conservation is a key test of simulation accuracy!
        If total energy drifts significantly, the time step may be too large.

        Note: Wall collisions are elastic, so they conserve kinetic energy.

        Returns:
            Tuple of (kinetic_energy, potential_energy, total_energy) in kcal/mol
        """
        # Kinetic energy: sum of both particles' KE
        ke = self.particle1.kinetic_energy + self.particle2.kinetic_energy

        # Potential energy: depends on distance between particles
        r_vector = self.particle1.position - self.particle2.position
        r = np.linalg.norm(r_vector)
        pe = self.potential.potential(r)

        # Total energy (should be conserved in microcanonical ensemble)
        total = ke + pe

        return ke, pe, total

    def _record_state(self) -> None:
        """
        Record current state to history for later analysis.

        This is called after each time step to build up trajectory data.
        """
        ke, pe, total = self.get_energies()

        self.history['time'].append(self.time)
        self.history['pos1'].append(self.particle1.position.copy())
        self.history['pos2'].append(self.particle2.position.copy())
        self.history['vel1'].append(self.particle1.velocity.copy())
        self.history['vel2'].append(self.particle2.velocity.copy())
        self.history['kinetic'].append(ke)
        self.history['potential'].append(pe)
        self.history['total'].append(total)
        self.history['wall_collisions_1'].append(self.wall_collision_count_1)
        self.history['wall_collisions_2'].append(self.wall_collision_count_2)

    def run(self, n_steps: int, record_interval: int = 1) -> None:
        """
        Run the simulation for a specified number of time steps.

        Args:
            n_steps: Number of time steps to simulate
            record_interval: Record state every N steps (default: 1 = every step)
                           Use larger values to save memory for long simulations
        """
        print(f"Starting 2D box simulation for {n_steps} steps (dt={self.dt} fs)...")
        print(f"Total simulation time: {n_steps * self.dt:.3f} fs")
        print(f"Box size: {self.box_size[0]} x {self.box_size[1]} Angstroms")

        # Record initial state
        self._record_state()

        # Main simulation loop
        for step in range(n_steps):
            self.step()

            # Record state at specified intervals
            if (step + 1) % record_interval == 0:
                self._record_state()

            # Progress indicator for long simulations
            if n_steps >= 10 and (step + 1) % (n_steps // 10) == 0:
                progress = 100 * (step + 1) / n_steps
                print(f"Progress: {progress:.0f}%")

        print("Simulation complete!")
        print(f"Particle 1 wall collisions: {self.wall_collision_count_1}")
        print(f"Particle 2 wall collisions: {self.wall_collision_count_2}")
        self._print_energy_statistics()

    def _print_energy_statistics(self) -> None:
        """Print statistics about energy conservation during the simulation."""
        if len(self.history['total']) < 2:
            return

        total_energies = np.array(self.history['total'])
        initial_energy = total_energies[0]
        final_energy = total_energies[-1]
        energy_drift = final_energy - initial_energy
        relative_drift = abs(energy_drift / initial_energy) * 100

        print(f"\nEnergy Statistics:")
        print(f"  Initial total energy: {initial_energy:.6f} kcal/mol")
        print(f"  Final total energy:   {final_energy:.6f} kcal/mol")
        print(f"  Energy drift:         {energy_drift:.6e} kcal/mol")
        print(f"  Relative drift:       {relative_drift:.4f}%")

        if relative_drift < 0.1:
            print("  [OK] Excellent energy conservation!")
        elif relative_drift < 1.0:
            print("  [OK] Good energy conservation")
        else:
            print("  [WARNING] Significant energy drift. Consider smaller time step.")

    def plot_trajectory(self) -> None:
        """
        Visualize the trajectories of both particles in the 2D box.

        Shows the box boundaries and the paths of both particles with
        different colors.
        """
        if len(self.history['pos1']) == 0:
            print("No trajectory data to plot. Run simulation first!")
            return

        # Convert position lists to numpy arrays
        pos1 = np.array(self.history['pos1'])
        pos2 = np.array(self.history['pos2'])

        # Create 2D plot
        plt.figure(figsize=(10, 10))

        # Draw box boundaries
        width, height = self.box_size
        plt.plot([0, width, width, 0, 0], [0, 0, height, height, 0],
                'k-', linewidth=2)

        # Plot trajectory of particle 1
        plt.plot(pos1[:, 0], pos1[:, 1],
                'b-', alpha=0.6, linewidth=1.5, label='Particle 1 path')

        # Plot trajectory of particle 2
        plt.plot(pos2[:, 0], pos2[:, 1],
                'r-', alpha=0.6, linewidth=1.5, label='Particle 2 path')

        # Mark starting positions
        plt.scatter([pos1[0, 0]], [pos1[0, 1]],
                   c='blue', marker='x', s=200, label='Start 1',
                   linewidths=2, zorder=5)
        plt.scatter([pos2[0, 0]], [pos2[0, 1]],
                   c='red', marker='x', s=200, label='Start 2',
                   linewidths=2, zorder=5)

        # Mark ending positions
        plt.scatter([pos1[-1, 0]], [pos1[-1, 1]],
                   facecolors='none', marker='o', s=200, label='End 1',
                   edgecolors='blue', linewidths=2, zorder=5)
        plt.scatter([pos2[-1, 0]], [pos2[-1, 1]],
                   facecolors='none', marker='o', s=200, label='End 2',
                   edgecolors='red', linewidths=2, zorder=5)

        plt.xlabel('X (Angstrom)', fontsize=12)
        plt.ylabel('Y (Angstrom)', fontsize=12)
        plt.title('Particle Trajectories in 2D Box', fontsize=14)
        plt.legend(fontsize=10, loc='center left', bbox_to_anchor=(1, 0.5))
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.xlim(-0.5, width + 0.5)
        plt.ylim(-0.5, height + 0.5)

        plt.tight_layout()
        plt.show()

    def plot_energy(self) -> None:
        """
        Plot kinetic, potential, and total energy over time.

        This is crucial for verifying energy conservation!
        """
        if len(self.history['time']) == 0:
            print("No energy data to plot. Run simulation first!")
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        time = np.array(self.history['time'])

        # Top plot: All energy components
        ax1.plot(time, self.history['kinetic'], 'b-', label='Kinetic Energy', linewidth=1.5)
        ax1.plot(time, self.history['potential'], 'r-', label='Potential Energy', linewidth=1.5)
        ax1.plot(time, self.history['total'], 'k-', label='Total Energy', linewidth=2)
        ax1.set_xlabel('Time (fs)')
        ax1.set_ylabel('Energy (kcal/mol)')
        ax1.set_title('Energy Components vs Time')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Bottom plot: Total energy deviation (zoomed in to see drift)
        total_energy = np.array(self.history['total'])
        initial_energy = total_energy[0]
        energy_deviation = total_energy - initial_energy

        ax2.plot(time, energy_deviation, 'g-', linewidth=1.5)
        ax2.set_xlabel('Time (fs)')
        ax2.set_ylabel('Energy Deviation (kcal/mol)')
        ax2.set_title('Total Energy Conservation (deviation from initial)')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)

        plt.tight_layout()
        plt.show()

    def plot_distance(self) -> None:
        """
        Plot the distance between particles over time.

        This helps visualize oscillations and whether particles are bound or unbound.
        """
        if len(self.history['pos1']) == 0:
            print("No trajectory data to plot. Run simulation first!")
            return

        # Calculate distances at each time step
        pos1 = np.array(self.history['pos1'])
        pos2 = np.array(self.history['pos2'])

        # Distance between particles
        distances = np.linalg.norm(pos1 - pos2, axis=1)

        plt.figure(figsize=(12, 6))
        plt.plot(self.history['time'], distances, 'purple', linewidth=1.5)
        plt.xlabel('Time (fs)', fontsize=12)
        plt.ylabel('Distance (Angstrom)', fontsize=12)
        plt.title('Inter-particle Distance vs Time', fontsize=14)
        plt.grid(True, alpha=0.3)

        # Add reference line for equilibrium distance (minimum of LJ potential)
        r_eq = 2 ** (1/6) * self.potential.sigma
        plt.axhline(y=r_eq, color='red', linestyle='--',
                   label=f'Equilibrium distance = {r_eq:.3f} A')
        plt.legend(fontsize=10)

        plt.tight_layout()
        plt.show()


# Example usage and demonstration
if __name__ == "__main__":
    """
    Demonstration of the two-particle MD simulation in a 2D box.

    This example simulates:
    - Two particles starting at different random positions
    - Both particles have the same initial velocity
    - Lennard-Jones interaction between them
    - Elastic collisions with box walls
    """
    print("=" * 70)
    print("Two-Particle Molecular Dynamics Simulation in 2D Box")
    print("=" * 70)

    # Set random seed for reproducibility
    random_seed = 42
    np.random.seed(random_seed)
    print(f"Random seed: {random_seed}")

    # Lennard-Jones parameters for Argon-Argon interaction
    # These are typical values from literature
    epsilon = 0.238  # kcal/mol (depth of potential well)
    sigma = 3.4      # Angstrom (collision diameter)

    # Create Lennard-Jones potential
    lj_potential = LennardJonesPotential(epsilon=epsilon, sigma=sigma)

    # Define box size (20 x 20 Angstroms)
    box_size = (20.0, 20.0)

    # Generate random positions for both particles
    # Ensure they start at least 2*sigma apart to avoid extreme forces
    min_separation = 2.0 * sigma

    while True:
        # Random positions within the box (with some margin from walls)
        pos1 = np.random.uniform(2.0, box_size[0] - 2.0, size=2)
        pos2 = np.random.uniform(2.0, box_size[1] - 2.0, size=2)

        # Check if particles are far enough apart
        separation = np.linalg.norm(pos1 - pos2)
        if separation >= min_separation:
            break

    print(f"Particle 1 starting position: [{pos1[0]:.2f}, {pos1[1]:.2f}]")
    print(f"Particle 2 starting position: [{pos2[0]:.2f}, {pos2[1]:.2f}]")
    print(f"Initial separation: {separation:.2f} Angstroms")

    # Initial velocity
    initial_velocity = np.array([0.02, 0.02])  # Angstroms/fs
    print(f"Initial velocity (particle 1): [{initial_velocity[0]:.3f}, {initial_velocity[1]:.3f}] A/fs")

    # Create particle 1
    particle1 = Particle(
        position=pos1,
        velocity=initial_velocity.copy(),  # Use copy to avoid reference issues
        mass=39.948,  # Argon mass in amu
        is_fixed=False
    )

    # Create particle 2 with same velocity
    particle2 = Particle(
        position=pos2,
        velocity=np.array([0.0, 0.0]),
        mass=39.948,  # Argon mass in amu
        is_fixed=True
    )

    # Create simulation
    # Time step: 1 fs is typical for MD simulations
    sim = TwoParticleMD(
        particle1=particle1,
        particle2=particle2,
        potential=lj_potential,
        box_size=box_size,
        dt=1.0  # 1 femtosecond time step
    )

    # Run simulation for 5000 steps = 5 picoseconds
    # This gives enough time to see multiple interactions and wall bounces
    sim.run(n_steps=5000, record_interval=1)

    # Visualize results
    print("\nGenerating plots...")
    sim.plot_trajectory()  # 2D trajectory in box
    #sim.plot_energy()      # Energy conservation check
    #sim.plot_distance()    # Distance between particles over time

    print("\nSimulation complete!")