"""
Streamlit App for Two-Particle MD Simulation

This app provides an interactive interface to:
1. Configure simulation parameters
2. Run the MD simulation
3. Visualize results (trajectory, energy, distance plots)
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from md_simulation import Particle, LennardJonesPotential, TwoParticleMD


def create_trajectory_figure(sim):
    """Create trajectory plot and return the figure."""
    if len(sim.history['pos1']) == 0:
        return None
    
    pos1 = np.array(sim.history['pos1'])
    pos2 = np.array(sim.history['pos2'])
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Draw box boundaries
    width, height = sim.box_size
    ax.plot([0, width, width, 0, 0], [0, 0, height, height, 0], 'k-', linewidth=2)
    
    # Plot trajectories
    ax.plot(pos1[:, 0], pos1[:, 1], 'b-', alpha=0.6, linewidth=1.5, label='Particle 1 path')
    ax.plot(pos2[:, 0], pos2[:, 1], 'r-', alpha=0.6, linewidth=1.5, label='Particle 2 path')
    
    # Mark starting positions
    ax.scatter([pos1[0, 0]], [pos1[0, 1]], c='blue', marker='x', s=200, label='Start 1', linewidths=2, zorder=5)
    ax.scatter([pos2[0, 0]], [pos2[0, 1]], c='red', marker='x', s=200, label='Start 2', linewidths=2, zorder=5)
    
    # Mark ending positions
    ax.scatter([pos1[-1, 0]], [pos1[-1, 1]], facecolors='none', marker='o', s=200, label='End 1', edgecolors='blue', linewidths=2, zorder=5)
    ax.scatter([pos2[-1, 0]], [pos2[-1, 1]], facecolors='none', marker='o', s=200, label='End 2', edgecolors='red', linewidths=2, zorder=5)
    
    ax.set_xlabel('X (Angstrom)', fontsize=12)
    ax.set_ylabel('Y (Angstrom)', fontsize=12)
    ax.set_title('Particle Trajectories in 2D Box', fontsize=14)
    ax.legend(fontsize=10, loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, width + 0.5)
    ax.set_ylim(-0.5, height + 0.5)
    
    plt.tight_layout()
    return fig


def create_energy_figure(sim):
    """Create energy plot and return the figure."""
    if len(sim.history['time']) == 0:
        return None
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    time = np.array(sim.history['time'])
    
    # Top plot: All energy components
    ax1.plot(time, sim.history['kinetic'], 'b-', label='Kinetic Energy', linewidth=1.5)
    ax1.plot(time, sim.history['potential'], 'r-', label='Potential Energy', linewidth=1.5)
    ax1.plot(time, sim.history['total'], 'k-', label='Total Energy', linewidth=2)
    ax1.set_xlabel('Time (fs)')
    ax1.set_ylabel('Energy (kcal/mol)')
    ax1.set_title('Energy Components vs Time')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Bottom plot: Total energy deviation
    total_energy = np.array(sim.history['total'])
    initial_energy = total_energy[0]
    energy_deviation = total_energy - initial_energy
    
    ax2.plot(time, energy_deviation, 'g-', linewidth=1.5)
    ax2.set_xlabel('Time (fs)')
    ax2.set_ylabel('Energy Deviation (kcal/mol)')
    ax2.set_title('Total Energy Deviation from Initial')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    return fig


def create_distance_figure(sim):
    """Create distance plot and return the figure."""
    if len(sim.history['pos1']) == 0:
        return None
    
    pos1 = np.array(sim.history['pos1'])
    pos2 = np.array(sim.history['pos2'])
    distances = np.linalg.norm(pos1 - pos2, axis=1)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sim.history['time'], distances, 'purple', linewidth=1.5)
    ax.set_xlabel('Time (fs)', fontsize=12)
    ax.set_ylabel('Distance (Angstrom)', fontsize=12)
    ax.set_title('Inter-particle Distance vs Time', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # Add reference line for equilibrium distance
    r_eq = 2 ** (1/6) * sim.potential.sigma
    ax.axhline(y=r_eq, color='red', linestyle='--', label=f'Equilibrium distance = {r_eq:.3f} A')
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    return fig


def main():
    st.set_page_config(
        page_title="MD Simulation",
        page_icon="🔬",
        layout="wide"
    )
    
    st.title("🔬 Two-Particle Molecular Dynamics Simulation")
    st.markdown("Interactive simulation of two particles interacting via Lennard-Jones potential in a 2D box.")
    
    # Sidebar for parameters
    st.sidebar.header("⚙️ Simulation Parameters")
    
    # Lennard-Jones parameters
    st.sidebar.subheader("Lennard-Jones Potential")
    epsilon = st.sidebar.number_input("Epsilon (kcal/mol)", value=0.238, min_value=0.001, format="%.3f")
    sigma = st.sidebar.number_input("Sigma (Angstrom)", value=3.4, min_value=0.1, format="%.2f")
    
    # Box parameters
    st.sidebar.subheader("Simulation Box")
    box_width = st.sidebar.number_input("Box Width (Angstrom)", value=20.0, min_value=5.0, format="%.1f")
    box_height = st.sidebar.number_input("Box Height (Angstrom)", value=20.0, min_value=5.0, format="%.1f")
    
    # Simulation parameters
    st.sidebar.subheader("Time Integration")
    dt = st.sidebar.number_input("Time Step (fs)", value=1.0, min_value=0.001, max_value=10.0, format="%.3f")
    n_steps = st.sidebar.number_input("Number of Steps", value=5000, min_value=100, max_value=100000, step=100)
    
    # Random seed
    st.sidebar.subheader("Random Seed")
    random_seed = st.sidebar.number_input("Seed", value=42, min_value=0, step=1)
    
    # Particle 1 parameters
    st.sidebar.subheader("Particle 1")
    mass1 = st.sidebar.number_input("Mass 1 (amu)", value=39.948, min_value=0.1, format="%.3f")
    vel1_x = st.sidebar.number_input("Velocity 1 X (A/fs)", value=0.02, format="%.4f")
    vel1_y = st.sidebar.number_input("Velocity 1 Y (A/fs)", value=0.02, format="%.4f")
    fixed1 = st.sidebar.checkbox("Fixed Particle 1", value=False)
    
    # Particle 2 parameters
    st.sidebar.subheader("Particle 2")
    mass2 = st.sidebar.number_input("Mass 2 (amu)", value=39.948, min_value=0.1, format="%.3f")
    vel2_x = st.sidebar.number_input("Velocity 2 X (A/fs)", value=0.0, format="%.4f")
    vel2_y = st.sidebar.number_input("Velocity 2 Y (A/fs)", value=0.0, format="%.4f")
    fixed2 = st.sidebar.checkbox("Fixed Particle 2", value=True)

    # Run simulation button
    run_button = st.sidebar.button("🚀 Run Simulation", type="primary", use_container_width=True)

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 Current Parameters")
        st.markdown(f"""
        **Lennard-Jones:** ε = {epsilon} kcal/mol, σ = {sigma} Å
        **Box Size:** {box_width} × {box_height} Å
        **Time Step:** {dt} fs, **Steps:** {n_steps}
        **Total Time:** {n_steps * dt:.1f} fs
        **Random Seed:** {random_seed}
        """)

    with col2:
        st.subheader("🔴🔵 Particle Configuration")
        st.markdown(f"""
        **Particle 1:** mass = {mass1} amu, v = ({vel1_x}, {vel1_y}) Å/fs {"[FIXED]" if fixed1 else ""}
        **Particle 2:** mass = {mass2} amu, v = ({vel2_x}, {vel2_y}) Å/fs {"[FIXED]" if fixed2 else ""}
        """)

    # Run simulation when button is clicked
    if run_button:
        # Set random seed
        np.random.seed(random_seed)

        # Create potential
        lj = LennardJonesPotential(epsilon=epsilon, sigma=sigma)

        # Generate random positions with minimum separation
        min_separation = 2.0 * sigma
        max_attempts = 100

        for attempt in range(max_attempts):
            pos1 = np.array([
                np.random.uniform(sigma, box_width - sigma),
                np.random.uniform(sigma, box_height - sigma)
            ])
            pos2 = np.array([
                np.random.uniform(sigma, box_width - sigma),
                np.random.uniform(sigma, box_height - sigma)
            ])

            if np.linalg.norm(pos1 - pos2) >= min_separation:
                break

        # Create particles
        particle1 = Particle(
            position=pos1,
            velocity=np.array([vel1_x, vel1_y]),
            mass=mass1,
            is_fixed=fixed1
        )

        particle2 = Particle(
            position=pos2,
            velocity=np.array([vel2_x, vel2_y]),
            mass=mass2,
            is_fixed=fixed2
        )

        # Show initial positions
        st.info(f"**Initial Positions:** Particle 1 at ({pos1[0]:.2f}, {pos1[1]:.2f}), Particle 2 at ({pos2[0]:.2f}, {pos2[1]:.2f})")

        # Create and run simulation
        with st.spinner("Running simulation..."):
            sim = TwoParticleMD(
                particle1=particle1,
                particle2=particle2,
                potential=lj,
                box_size=(box_width, box_height),
                dt=dt
            )

            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Run simulation with progress updates
            sim.history['time'].append(sim.time)
            sim.history['pos1'].append(sim.particle1.position.copy())
            sim.history['pos2'].append(sim.particle2.position.copy())
            sim.history['vel1'].append(sim.particle1.velocity.copy())
            sim.history['vel2'].append(sim.particle2.velocity.copy())
            ke, pe, total = sim.get_energies()
            sim.history['kinetic'].append(ke)
            sim.history['potential'].append(pe)
            sim.history['total'].append(total)
            sim.history['wall_collisions_1'].append(sim.wall_collision_count_1)
            sim.history['wall_collisions_2'].append(sim.wall_collision_count_2)

            for step in range(n_steps):
                sim.step()

                # Record state
                sim.history['time'].append(sim.time)
                sim.history['pos1'].append(sim.particle1.position.copy())
                sim.history['pos2'].append(sim.particle2.position.copy())
                sim.history['vel1'].append(sim.particle1.velocity.copy())
                sim.history['vel2'].append(sim.particle2.velocity.copy())
                ke, pe, total = sim.get_energies()
                sim.history['kinetic'].append(ke)
                sim.history['potential'].append(pe)
                sim.history['total'].append(total)
                sim.history['wall_collisions_1'].append(sim.wall_collision_count_1)
                sim.history['wall_collisions_2'].append(sim.wall_collision_count_2)

                # Update progress every 1%
                if (step + 1) % max(1, n_steps // 100) == 0:
                    progress = (step + 1) / n_steps
                    progress_bar.progress(progress)
                    status_text.text(f"Progress: {progress * 100:.0f}% ({step + 1}/{n_steps} steps)")

            progress_bar.progress(1.0)
            status_text.text("Simulation complete!")

        # Store simulation in session state
        st.session_state['simulation'] = sim

        # Display results
        st.success(f"✅ Simulation completed! Wall collisions: Particle 1 = {sim.wall_collision_count_1}, Particle 2 = {sim.wall_collision_count_2}")

        # Energy statistics
        total_energies = np.array(sim.history['total'])
        initial_energy = total_energies[0]
        final_energy = total_energies[-1]
        energy_drift = final_energy - initial_energy
        relative_drift = abs(energy_drift / initial_energy) * 100 if initial_energy != 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Initial Energy", f"{initial_energy:.4f} kcal/mol")
        col2.metric("Final Energy", f"{final_energy:.4f} kcal/mol")
        col3.metric("Energy Drift", f"{energy_drift:.2e} kcal/mol")
        col4.metric("Relative Drift", f"{relative_drift:.4f}%")

    # Display plots if simulation exists
    if 'simulation' in st.session_state:
        sim = st.session_state['simulation']

        st.markdown("---")
        st.header("📊 Visualization")

        # Plot tabs
        tab1, tab2, tab3 = st.tabs(["🗺️ Trajectory", "⚡ Energy", "📏 Distance"])

        with tab1:
            fig_traj = create_trajectory_figure(sim)
            if fig_traj:
                st.pyplot(fig_traj)
                plt.close(fig_traj)

        with tab2:
            fig_energy = create_energy_figure(sim)
            if fig_energy:
                st.pyplot(fig_energy)
                plt.close(fig_energy)

        with tab3:
            fig_dist = create_distance_figure(sim)
            if fig_dist:
                st.pyplot(fig_dist)
                plt.close(fig_dist)


if __name__ == "__main__":
    main()

