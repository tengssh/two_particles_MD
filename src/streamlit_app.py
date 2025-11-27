"""
Streamlit App for Two-Particle MD Simulation

This app provides an interactive interface to:
1. Configure simulation parameters
2. Run the MD simulation
3. Visualize results (trajectory, energy, distance plots)
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add the src directory to the path for imports
_src_dir = os.path.dirname(os.path.abspath(__file__))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

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


def create_plotly_animated_trajectory(sim, frame_step=10):
    """Create Plotly animated trajectory with growing paths, slider and play/pause controls.

    Args:
        sim: TwoParticleMD simulation object with history
        frame_step: Step size for animation frames (to reduce total frames)

    Returns:
        Plotly figure with animation slider and controls
    """
    if len(sim.history['pos1']) == 0:
        return None

    pos1 = np.array(sim.history['pos1'])
    pos2 = np.array(sim.history['pos2'])
    times = sim.history['time']
    width, height = sim.box_size

    n_frames = len(pos1)
    # Sample frames to keep animation smooth
    frame_indices = list(range(0, n_frames, max(1, frame_step)))
    if frame_indices[-1] != n_frames - 1:
        frame_indices.append(n_frames - 1)

    # Build DataFrame for Plotly Express to get working slider infrastructure
    data_rows = []
    for idx in frame_indices:
        time_label = f"{times[idx]:.1f} fs"
        data_rows.append({
            'x': pos1[idx, 0], 'y': pos1[idx, 1],
            'particle': 'Particle 1', 'frame': time_label, 'frame_idx': idx
        })
        data_rows.append({
            'x': pos2[idx, 0], 'y': pos2[idx, 1],
            'particle': 'Particle 2', 'frame': time_label, 'frame_idx': idx
        })

    df = pd.DataFrame(data_rows)

    # Create base figure with Plotly Express (this gives us working slider)
    fig = px.scatter(
        df, x='x', y='y', color='particle', animation_frame='frame',
        color_discrete_map={'Particle 1': 'blue', 'Particle 2': 'red'},
        range_x=[-0.5, width + 0.5], range_y=[-0.5, height + 0.5],
        title='Particle Trajectory Animation',
        labels={'x': 'X (Angstrom)', 'y': 'Y (Angstrom)'},
    )

    # Make current position markers larger
    fig.update_traces(marker=dict(size=18, line=dict(width=2, color='DarkSlateGrey')))

    # Add box boundary as static shape
    fig.add_shape(type="rect", x0=0, y0=0, x1=width, y1=height,
                  line=dict(color="black", width=2))

    # Add start position markers (static, will appear in all frames)
    fig.add_trace(go.Scatter(
        x=[pos1[0, 0]], y=[pos1[0, 1]], mode='markers',
        marker=dict(symbol='x', size=15, color='blue', line=dict(width=2)),
        name='Start 1', showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[pos2[0, 0]], y=[pos2[0, 1]], mode='markers',
        marker=dict(symbol='x', size=15, color='red', line=dict(width=2)),
        name='Start 2', showlegend=True
    ))

    # Add initial trajectory traces (empty, will be populated in frames)
    fig.add_trace(go.Scatter(
        x=[pos1[0, 0]], y=[pos1[0, 1]], mode='lines',
        line=dict(color='blue', width=2), opacity=0.6,
        name='Path 1', showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[pos2[0, 0]], y=[pos2[0, 1]], mode='lines',
        line=dict(color='red', width=2), opacity=0.6,
        name='Path 2', showlegend=True
    ))

    # Now modify each frame to include growing trajectory paths
    # The px.scatter creates frames with 2 traces (Particle 1, Particle 2)
    # We need to add: Start1, Start2, Path1, Path2 to each frame
    for i, frame in enumerate(fig.frames):
        idx = frame_indices[i]
        # Get existing particle position traces from the frame
        existing_data = list(frame.data)

        # Add static start markers
        existing_data.append(go.Scatter(
            x=[pos1[0, 0]], y=[pos1[0, 1]], mode='markers',
            marker=dict(symbol='x', size=15, color='blue', line=dict(width=2)),
            name='Start 1'
        ))
        existing_data.append(go.Scatter(
            x=[pos2[0, 0]], y=[pos2[0, 1]], mode='markers',
            marker=dict(symbol='x', size=15, color='red', line=dict(width=2)),
            name='Start 2'
        ))

        # Add growing trajectory paths (up to current frame)
        existing_data.append(go.Scatter(
            x=pos1[:idx+1, 0].tolist(), y=pos1[:idx+1, 1].tolist(),
            mode='lines', line=dict(color='blue', width=2), opacity=0.6,
            name='Path 1'
        ))
        existing_data.append(go.Scatter(
            x=pos2[:idx+1, 0].tolist(), y=pos2[:idx+1, 1].tolist(),
            mode='lines', line=dict(color='red', width=2), opacity=0.6,
            name='Path 2'
        ))

        # Update the frame with new data
        frame.data = tuple(existing_data)

    # Update layout
    fig.update_layout(
        height=650,
        xaxis=dict(scaleanchor='y', scaleratio=1),
        legend=dict(x=1.02, y=0.5, xanchor='left'),
        updatemenus=[{
            'buttons': [
                {'args': [None, {'frame': {'duration': 100, 'redraw': True},
                                'fromcurrent': True, 'transition': {'duration': 0}}],
                 'label': '▶ Play', 'method': 'animate'},
                {'args': [[None], {'frame': {'duration': 0, 'redraw': False},
                                  'mode': 'immediate', 'transition': {'duration': 0}}],
                 'label': '⏸ Pause', 'method': 'animate'}
            ],
            'direction': 'left', 'pad': {'r': 10, 't': 70},
            'showactive': False, 'type': 'buttons',
            'x': 0.1, 'xanchor': 'right', 'y': 0, 'yanchor': 'top'
        }],
        sliders=[{
            'active': 0, 'yanchor': 'top', 'xanchor': 'left',
            'currentvalue': {'font': {'size': 14}, 'prefix': 'Time: ',
                           'visible': True, 'xanchor': 'center'},
            'transition': {'duration': 0}, 'pad': {'b': 10, 't': 50},
            'len': 0.9, 'x': 0.1, 'y': 0,
            'steps': fig.layout.sliders[0].steps if fig.layout.sliders else []
        }]
    )

    return fig


def main():
    st.set_page_config(
        page_title="MD Simulation",
        page_icon="🔬",
        layout="wide"
    )

    # ==================== TOP SECTION: Title and Description ====================
    st.title("🔬 Two-Particle Molecular Dynamics Simulation")
    st.markdown("""
    Interactive simulation of two particles interacting via **Lennard-Jones potential** in a 2D box.
    Configure parameters below, run the simulation, and visualize the results.
    """)
    st.markdown("---")

    # ==================== MIDDLE SECTION: Parameters and Run Button ====================
    st.header("⚙️ Simulation Parameters")

    # Create columns for parameter inputs
    param_col1, param_col2, param_col3 = st.columns(3)

    with param_col1:
        st.subheader("Lennard-Jones Potential")
        epsilon = st.number_input("Epsilon (kcal/mol)", value=0.238, min_value=0.001, format="%.3f")
        sigma = st.number_input("Sigma (Angstrom)", value=3.4, min_value=0.1, format="%.2f")

        st.subheader("Simulation Box")
        box_width = st.number_input("Box Width (Angstrom)", value=20.0, min_value=5.0, format="%.1f")
        box_height = st.number_input("Box Height (Angstrom)", value=20.0, min_value=5.0, format="%.1f")

    with param_col2:
        st.subheader("Time Integration")
        dt = st.number_input("Time Step (fs)", value=1.0, min_value=0.001, max_value=10.0, format="%.3f")
        n_steps = st.number_input("Number of Steps", value=5000, min_value=100, max_value=100000, step=100)
        random_seed = st.number_input("Random Seed", value=42, min_value=0, step=1)
        st.markdown(f"**Total Time:** {n_steps * dt:.1f} fs")

    with param_col3:
        st.subheader("Particle 1 🔵")
        mass1 = st.number_input("Mass 1 (amu)", value=39.948, min_value=0.1, format="%.3f")
        p1_vel_col1, p1_vel_col2 = st.columns(2)
        with p1_vel_col1:
            vel1_x = st.number_input("Vel 1 X (A/fs)", value=0.02, format="%.4f")
        with p1_vel_col2:
            vel1_y = st.number_input("Vel 1 Y (A/fs)", value=0.02, format="%.4f")
        fixed1 = st.checkbox("Fixed Particle 1", value=False)

        st.subheader("Particle 2 🔴")
        mass2 = st.number_input("Mass 2 (amu)", value=39.948, min_value=0.1, format="%.3f")
        p2_vel_col1, p2_vel_col2 = st.columns(2)
        with p2_vel_col1:
            vel2_x = st.number_input("Vel 2 X (A/fs)", value=0.0, format="%.4f")
        with p2_vel_col2:
            vel2_y = st.number_input("Vel 2 Y (A/fs)", value=0.0, format="%.4f")
        fixed2 = st.checkbox("Fixed Particle 2", value=True)

    # Run simulation button (centered)
    st.markdown("")
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
    with btn_col2:
        run_button = st.button("🚀 Run Simulation", type="primary", use_container_width=True)

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

    # ==================== BOTTOM SECTION: Visualization ====================
    # Display plots if simulation exists
    if 'simulation' in st.session_state:
        sim = st.session_state['simulation']

        st.markdown("---")
        st.header("📊 Visualization")

        # Two main tabs: Static Outputs and Interactive
        tab_static, tab_interactive = st.tabs(["📈 Static Outputs", "🎬 Interactive Trajectory"])

        # Tab 1: All static figures displayed at once
        with tab_static:
            st.subheader("Complete Simulation Results")

            # Trajectory plot
            st.markdown("### 🗺️ Particle Trajectories")
            fig_traj = create_trajectory_figure(sim)
            if fig_traj:
                st.pyplot(fig_traj)
                plt.close(fig_traj)

            st.markdown("---")

            # Energy plot
            st.markdown("### ⚡ Energy Analysis")
            fig_energy = create_energy_figure(sim)
            if fig_energy:
                st.pyplot(fig_energy)
                plt.close(fig_energy)

            st.markdown("---")

            # Distance plot
            st.markdown("### 📏 Inter-particle Distance")
            fig_dist = create_distance_figure(sim)
            if fig_dist:
                st.pyplot(fig_dist)
                plt.close(fig_dist)

        # Tab 2: Interactive trajectory viewer with Plotly Express animation
        with tab_interactive:
            st.subheader("🎬 Interactive Trajectory Viewer")
            st.markdown("""
            Use the **slider** to navigate through frames or click **Play/Pause** to animate.
            The full trajectory paths are shown in light colors, with current positions as large markers.
            """)

            n_frames = len(sim.history['pos1'])
            if n_frames > 1:
                # Calculate default frame step based on number of frames (aim for ~100 frames max)
                default_step = max(1, n_frames // 100)

                # Create and display Plotly Express animated figure
                fig_plotly = create_plotly_animated_trajectory(sim, frame_step=default_step)
                if fig_plotly:
                    st.plotly_chart(fig_plotly, use_container_width=True)

                # Display summary info
                st.markdown("**Simulation Summary:**")
                info_col1, info_col2, info_col3 = st.columns(3)
                info_col1.metric("Total Frames", n_frames)
                info_col2.metric("Total Time", f"{sim.history['time'][-1]:.1f} fs")
                info_col3.metric("Animation Frames", len(range(0, n_frames, max(1, default_step))) + 1)
            else:
                st.warning("Not enough frames to display interactive trajectory.")


if __name__ == "__main__":
    main()

