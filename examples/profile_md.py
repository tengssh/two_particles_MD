"""
Performance Profiling Example for MD Simulation

This script demonstrates various profiling techniques applied to the
two-particle MD simulation.

Usage:
    # Basic profiling
    python profile_md.py
    
    # With line profiler
    kernprof -l -v profile_md.py
    
    # With memory profiler
    python -m memory_profiler profile_md.py

Requirements:
    pip install line_profiler memory_profiler
"""

import sys
import os
import time
import cProfile
import pstats
from io import StringIO

# Add parent directory to path to import md_simulation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from md_simulation import TwoParticleMD, Particle, LennardJonesPotential
import numpy as np


def simple_timing():
    """Demonstrate simple timing with time.perf_counter()."""
    print("=" * 70)
    print("1. Simple Timing (time.perf_counter)")
    print("=" * 70)
    
    # Create simulation
    particle1 = Particle(position=np.array([5.0, 5.0]), velocity=np.array([0.1, 0.0]), is_fixed=True)
    particle2 = Particle(position=np.array([8.0, 5.0]), velocity=np.array([-0.05, 0.0]))
    potential = LennardJonesPotential()
    sim = TwoParticleMD(particle1, particle2, potential, box_size=(20.0, 20.0))
    
    # Time initialization
    start = time.perf_counter()
    sim = TwoParticleMD(particle1, particle2, potential, box_size=(20.0, 20.0))
    init_time = time.perf_counter() - start
    print(f"Initialization time: {init_time*1000:.4f} ms")
    
    # Time single step
    start = time.perf_counter()
    sim.step()
    step_time = time.perf_counter() - start
    print(f"Single step time: {step_time*1000:.4f} ms")
    
    # Time 1000 steps
    start = time.perf_counter()
    sim.run(1000, record_interval=100)
    run_time = time.perf_counter() - start
    print(f"1000 steps time: {run_time:.4f} s")
    print(f"Average per step: {run_time/1000*1000:.4f} ms")
    print()


def cprofile_analysis():
    """Demonstrate cProfile for function-level profiling."""
    print("=" * 70)
    print("2. Function-Level Profiling (cProfile)")
    print("=" * 70)
    
    # Create simulation
    particle1 = Particle(position=np.array([5.0, 5.0]), velocity=np.array([0.1, 0.0]), is_fixed=True)
    particle2 = Particle(position=np.array([8.0, 5.0]), velocity=np.array([-0.05, 0.0]))
    potential = LennardJonesPotential()
    sim = TwoParticleMD(particle1, particle2, potential, box_size=(20.0, 20.0))
    
    # Profile the simulation
    profiler = cProfile.Profile()
    profiler.enable()
    
    sim.run(1000, record_interval=100)
    
    profiler.disable()
    
    # Print statistics
    s = StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats('cumulative')
    stats.print_stats(15)  # Top 15 functions
    
    print(s.getvalue())
    print()


def component_timing():
    """Time individual components of the simulation."""
    print("=" * 70)
    print("3. Component-Level Timing")
    print("=" * 70)

    # Create simulation
    particle1 = Particle(position=np.array([5.0, 5.0]), velocity=np.array([0.1, 0.0]), is_fixed=True)
    particle2 = Particle(position=np.array([8.0, 5.0]), velocity=np.array([-0.05, 0.0]))
    potential = LennardJonesPotential()
    sim = TwoParticleMD(particle1, particle2, potential, box_size=(20.0, 20.0))

    n_iterations = 1000

    # Time single step (includes force calculation, integration, boundaries)
    start = time.perf_counter()
    for _ in range(n_iterations):
        sim.step()
    step_time = time.perf_counter() - start

    # Time energy calculation
    start = time.perf_counter()
    for _ in range(n_iterations):
        sim.get_energies()
    energy_time = time.perf_counter() - start

    # Time force calculation (via potential)
    start = time.perf_counter()
    for _ in range(n_iterations):
        r_vector = sim.particle1.position - sim.particle2.position
        r = np.linalg.norm(r_vector)
        force_mag = sim.potential.force_magnitude(r)
    force_calc_time = time.perf_counter() - start

    # Time position update (simplified)
    start = time.perf_counter()
    for _ in range(n_iterations):
        # Simulate position update
        temp_pos = sim.particle2.position + sim.particle2.velocity * sim.dt
    position_update_time = time.perf_counter() - start

    # Print results
    total_time = step_time + energy_time

    print(f"Component timing ({n_iterations} iterations):")
    print(f"  Full step (step()):       {step_time:.4f}s ({step_time/total_time*100:.1f}%)")
    print(f"  Energy calculation:       {energy_time:.4f}s ({energy_time/total_time*100:.1f}%)")
    print(f"  Force calculation only:   {force_calc_time:.4f}s (isolated)")
    print(f"  Position update only:     {position_update_time:.4f}s (isolated)")
    print(f"  Total:                    {total_time:.4f}s")
    print(f"\nAverage time per step: {step_time/n_iterations*1000:.4f} ms")
    print()


def memory_usage():
    """Demonstrate memory profiling with tracemalloc."""
    print("=" * 70)
    print("4. Memory Usage (tracemalloc)")
    print("=" * 70)
    
    import tracemalloc
    
    # Start tracing
    tracemalloc.start()
    
    # Create simulation
    particle1 = Particle(position=np.array([5.0, 5.0]), velocity=np.array([0.1, 0.0]), is_fixed=True)
    particle2 = Particle(position=np.array([8.0, 5.0]), velocity=np.array([-0.05, 0.0]))
    potential = LennardJonesPotential()
    sim = TwoParticleMD(particle1, particle2, potential, box_size=(20.0, 20.0))
    
    # Run simulation
    sim.run(1000, record_interval=10)
    
    # Get memory snapshot
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    
    print("Top 10 memory allocations:")
    for stat in top_stats[:10]:
        print(f"  {stat}")
    
    # Get current and peak memory
    current, peak = tracemalloc.get_traced_memory()
    print(f"\nCurrent memory usage: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
    
    tracemalloc.stop()
    print()


def scaling_analysis():
    """Analyze how performance scales with number of steps."""
    print("=" * 70)
    print("5. Scaling Analysis")
    print("=" * 70)

    particle1 = Particle(position=np.array([5.0, 5.0]), velocity=np.array([0.1, 0.0]), is_fixed=True)
    particle2 = Particle(position=np.array([8.0, 5.0]), velocity=np.array([-0.05, 0.0]))
    potential = LennardJonesPotential()

    step_counts = [100, 500, 1000, 5000, 10000]

    print(f"{'Steps':<10} {'Time (s)':<12} {'Time/Step (ms)':<18} {'Steps/sec':<12}")
    print("-" * 70)

    for n_steps in step_counts:
        sim = TwoParticleMD(particle1, particle2, potential, box_size=(20.0, 20.0))

        start = time.perf_counter()
        sim.run(n_steps, record_interval=max(n_steps//10, 1))
        elapsed = time.perf_counter() - start

        time_per_step = elapsed / n_steps * 1000  # ms
        steps_per_sec = n_steps / elapsed

        print(f"{n_steps:<10} {elapsed:<12.4f} {time_per_step:<18.6f} {steps_per_sec:<12.1f}")

    print()


def line_profiler_example():
    """Example for line_profiler (requires @profile decorator)."""
    print("=" * 70)
    print("6. Line-by-Line Profiling")
    print("=" * 70)
    print("To use line_profiler:")
    print("  1. Add @profile decorator to functions in md_simulation.py")
    print("  2. Run: kernprof -l -v profile_md.py")
    print()
    print("Example functions to profile:")
    print("  - TwoParticleMD.step()")
    print("  - TwoParticleMD.compute_forces()")
    print("  - LennardJonesPotential.compute_force()")
    print()


def recommendations():
    """Print profiling recommendations."""
    print("=" * 70)
    print("7. Profiling Recommendations")
    print("=" * 70)
    print()
    print("Based on the profiling results above, here are optimization strategies:")
    print()
    print("🎯 Quick Wins:")
    print("  1. Vectorize operations - Use NumPy array operations")
    print("  2. Reduce function calls - Inline small functions")
    print("  3. Cache results - Store frequently computed values")
    print()
    print("🚀 Advanced Optimizations:")
    print("  1. Use Numba JIT - Add @jit decorator to hot functions")
    print("  2. Parallel processing - Use multiprocessing for ensemble runs")
    print("  3. GPU acceleration - Offload to GPU for large systems")
    print()
    print("📊 Profiling Tools to Try:")
    print("  1. py-spy - Generate flame graphs:")
    print("     py-spy record -o profile.svg -- python profile_md.py")
    print()
    print("  2. SnakeViz - Visualize cProfile results:")
    print("     python -m cProfile -o profile.prof profile_md.py")
    print("     snakeviz profile.prof")
    print()
    print("  3. memory_profiler - Track memory usage:")
    print("     python -m memory_profiler profile_md.py")
    print()
    print("📚 See PROFILING_GUIDE.md for detailed documentation")
    print()


def main():
    """Run all profiling examples."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "MD Simulation Performance Profiling" + " " * 18 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    try:
        # Run profiling examples
        simple_timing()
        cprofile_analysis()
        component_timing()
        memory_usage()
        scaling_analysis()
        line_profiler_example()
        recommendations()

        print("=" * 70)
        print("✅ Profiling complete!")
        print("=" * 70)
        print()

    except Exception as e:
        print(f"❌ Error during profiling: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


