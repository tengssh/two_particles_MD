"""
Parallelization Examples for MD Simulation

This file demonstrates various parallelization techniques that can be applied
to extend the 2-particle simulation to N particles.

Examples include:
1. NumPy vectorization
2. Numba JIT compilation
3. Ensemble parallelism
4. GPU acceleration (PyTorch)
"""

import numpy as np
import time
from typing import Tuple

# Example 1: NumPy Vectorization
# ================================

def update_positions_loop(positions, velocities, dt, N):
    """Traditional loop-based position update (SLOW)."""
    for i in range(N):
        positions[i] += velocities[i] * dt
    return positions


def update_positions_vectorized(positions, velocities, dt):
    """Vectorized position update using NumPy (FAST)."""
    return positions + velocities * dt


def benchmark_vectorization():
    """Compare loop vs vectorized performance."""
    N = 10000
    positions = np.random.rand(N, 2) * 20.0
    velocities = np.random.rand(N, 2) * 0.1
    dt = 0.001
    
    # Loop version
    start = time.time()
    for _ in range(100):
        positions_loop = update_positions_loop(positions.copy(), velocities, dt, N)
    loop_time = time.time() - start
    
    # Vectorized version
    start = time.time()
    for _ in range(100):
        positions_vec = update_positions_vectorized(positions.copy(), velocities, dt)
    vec_time = time.time() - start
    
    print(f"Loop version: {loop_time:.4f}s")
    print(f"Vectorized version: {vec_time:.4f}s")
    print(f"Speedup: {loop_time/vec_time:.1f}x")


# Example 2: Numba JIT Compilation
# =================================

try:
    from numba import jit, prange
    
    @jit(nopython=True)
    def compute_lj_force_numba(r_vec, epsilon=1.0, sigma=1.0):
        """Compute Lennard-Jones force (Numba-optimized)."""
        r = np.sqrt(r_vec[0]**2 + r_vec[1]**2)
        if r < 1e-10:
            return np.zeros(2)
        
        sr6 = (sigma / r) ** 6
        force_mag = 24.0 * epsilon / r * (2.0 * sr6**2 - sr6)
        r_hat = r_vec / r
        return force_mag * r_hat
    
    @jit(nopython=True, parallel=True)
    def compute_all_forces_parallel(positions, N, epsilon=1.0, sigma=1.0):
        """Compute all pairwise forces in parallel."""
        forces = np.zeros_like(positions)
        
        # Parallel loop over particles
        for i in prange(N):
            for j in range(i+1, N):
                r_vec = positions[i] - positions[j]
                f = compute_lj_force_numba(r_vec, epsilon, sigma)
                forces[i] += f
                forces[j] -= f
        
        return forces
    
    def benchmark_numba():
        """Benchmark Numba parallel force calculation."""
        N = 1000
        positions = np.random.rand(N, 2) * 20.0
        
        # Warm-up (JIT compilation happens here)
        _ = compute_all_forces_parallel(positions, N)
        
        # Benchmark
        start = time.time()
        for _ in range(10):
            forces = compute_all_forces_parallel(positions, N)
        numba_time = time.time() - start
        
        print(f"Numba parallel force calculation: {numba_time:.4f}s for {N} particles")
        print(f"Time per iteration: {numba_time/10:.4f}s")
    
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    print("Numba not available. Install with: pip install numba")


# Example 3: Ensemble Parallelism
# ================================

def run_single_simulation(params):
    """Run a single simulation with given parameters."""
    temperature, n_steps = params
    
    # Simulate some work
    np.random.seed(int(temperature * 1000))
    positions = np.random.rand(100, 2) * 20.0
    velocities = np.random.rand(100, 2) * 0.1 * temperature
    
    # Simple integration
    dt = 0.001
    for _ in range(n_steps):
        positions += velocities * dt
    
    # Return some result
    avg_position = np.mean(positions)
    return temperature, avg_position


def run_ensemble_serial(temperatures, n_steps):
    """Run ensemble of simulations serially."""
    results = []
    for temp in temperatures:
        result = run_single_simulation((temp, n_steps))
        results.append(result)
    return results


def run_ensemble_parallel(temperatures, n_steps):
    """Run ensemble of simulations in parallel."""
    from multiprocessing import Pool
    
    params = [(temp, n_steps) for temp in temperatures]
    
    with Pool(processes=4) as pool:
        results = pool.map(run_single_simulation, params)
    
    return results


def benchmark_ensemble():
    """Compare serial vs parallel ensemble runs."""
    temperatures = [100, 200, 300, 400, 500, 600, 700, 800]
    n_steps = 1000
    
    # Serial
    start = time.time()
    results_serial = run_ensemble_serial(temperatures, n_steps)
    serial_time = time.time() - start
    
    # Parallel
    start = time.time()
    results_parallel = run_ensemble_parallel(temperatures, n_steps)
    parallel_time = time.time() - start
    
    print(f"Serial ensemble: {serial_time:.4f}s")
    print(f"Parallel ensemble: {parallel_time:.4f}s")
    print(f"Speedup: {serial_time/parallel_time:.1f}x")


# Example 4: GPU Acceleration with PyTorch
# =========================================

try:
    import torch
    
    def update_positions_gpu(positions, velocities, dt):
        """Update positions on GPU using PyTorch."""
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Move to GPU
        pos_gpu = torch.tensor(positions, device=device, dtype=torch.float32)
        vel_gpu = torch.tensor(velocities, device=device, dtype=torch.float32)
        
        # Compute on GPU
        pos_gpu += vel_gpu * dt
        
        # Move back to CPU
        return pos_gpu.cpu().numpy()
    
    def benchmark_gpu():
        """Benchmark GPU vs CPU for position updates."""
        N = 100000  # Large number for GPU to shine
        positions = np.random.rand(N, 2).astype(np.float32) * 20.0
        velocities = np.random.rand(N, 2).astype(np.float32) * 0.1
        dt = 0.001
        
        if not torch.cuda.is_available():
            print("CUDA not available. Running on CPU only.")
            device = torch.device('cpu')
        else:
            device = torch.device('cuda')
            print(f"Using GPU: {torch.cuda.get_device_name(0)}")
        
        # CPU version
        start = time.time()
        for _ in range(100):
            pos_cpu = update_positions_vectorized(positions.copy(), velocities, dt)
        cpu_time = time.time() - start
        
        # GPU version
        pos_gpu = torch.tensor(positions, device=device)
        vel_gpu = torch.tensor(velocities, device=device)
        
        # Warm-up
        _ = pos_gpu + vel_gpu * dt
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        
        start = time.time()
        for _ in range(100):
            pos_gpu += vel_gpu * dt
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        gpu_time = time.time() - start
        
        print(f"CPU (NumPy): {cpu_time:.4f}s")
        print(f"GPU (PyTorch): {gpu_time:.4f}s")
        if torch.cuda.is_available():
            print(f"Speedup: {cpu_time/gpu_time:.1f}x")
    
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch not available. Install with: pip install torch")


# Example 5: MPI (Message Passing Interface)
# ===========================================

MPI_EXAMPLE_CODE = '''
"""
MPI Example - Save this as mpi_example.py and run with:
    mpiexec -n 4 python mpi_example.py

This demonstrates basic MPI concepts for MD simulations.
"""

from mpi4py import MPI
import numpy as np
import time

def mpi_hello_world():
    """Basic MPI: Each process prints its rank."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    print(f"Hello from rank {rank} of {size} processes")
    return rank, size

def mpi_parallel_sum():
    """Demonstrate MPI reduction (sum across all processes)."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # Each process has a local value
    local_value = rank * 10

    # Sum across all processes
    total = comm.allreduce(local_value, op=MPI.SUM)

    if rank == 0:
        print(f"\\nMPI Reduction: Sum of all ranks = {total}")

    return total

def mpi_domain_decomposition():
    """Simulate domain decomposition for MD."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Total particles divided among processes
    total_particles = 1000
    local_n = total_particles // size

    # Each rank initializes its local particles
    np.random.seed(rank)
    local_positions = np.random.rand(local_n, 3) * 20.0
    local_velocities = np.random.rand(local_n, 3) * 0.1

    # Simulate some work (position update)
    dt = 0.001
    start = time.time()
    for _ in range(100):
        local_positions += local_velocities * dt
    elapsed = time.time() - start

    # Gather timing from all ranks
    all_times = comm.gather(elapsed, root=0)

    if rank == 0:
        print(f"\\nMPI Domain Decomposition:")
        print(f"  Total particles: {total_particles}")
        print(f"  Particles per rank: {local_n}")
        print(f"  Average time: {np.mean(all_times):.4f}s")
        print(f"  Max time: {np.max(all_times):.4f}s")
        print(f"  Min time: {np.min(all_times):.4f}s")

def mpi_replica_exchange():
    """Simulate replica exchange (each rank = different temperature)."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Each rank has different temperature
    base_temp = 300.0
    temperature = base_temp * (1.1 ** rank)

    print(f"Rank {rank}: Running at T = {temperature:.2f} K")

    # Simulate energy calculation
    np.random.seed(rank)
    energy = np.random.randn() * temperature

    # Exchange energies with neighbor
    if rank % 2 == 0 and rank + 1 < size:
        partner = rank + 1
        partner_energy = comm.sendrecv(energy, dest=partner, source=partner)

        if rank == 0:
            print(f"\\nReplica Exchange: Rank {rank} ↔ Rank {partner}")
            print(f"  Energy {rank}: {energy:.4f}")
            print(f"  Energy {partner}: {partner_energy:.4f}")

if __name__ == "__main__":
    # Run all MPI examples
    rank, size = mpi_hello_world()

    comm = MPI.COMM_WORLD
    comm.Barrier()  # Synchronize

    if rank == 0:
        print("\\n" + "=" * 60)

    mpi_parallel_sum()
    comm.Barrier()

    if rank == 0:
        print("=" * 60)

    mpi_domain_decomposition()
    comm.Barrier()

    if rank == 0:
        print("=" * 60)

    mpi_replica_exchange()

    if rank == 0:
        print("=" * 60)
        print("\\nMPI examples complete!")
        print("\\nTo run: mpiexec -n 4 python mpi_example.py")
'''

def show_mpi_info():
    """Show information about MPI and how to use it."""
    print("\n" + "=" * 60)
    print("MPI (Message Passing Interface) Information")
    print("=" * 60)

    try:
        from mpi4py import MPI
        print("✅ mpi4py is installed!")
        print(f"   MPI Version: {MPI.Get_version()}")

        # Save example code
        with open('mpi_example.py', 'w') as f:
            f.write(MPI_EXAMPLE_CODE)

        print("\n📝 MPI example saved to: mpi_example.py")
        print("\n🚀 To run MPI example:")
        print("   mpiexec -n 4 python mpi_example.py")
        print("\n💡 This will run 4 parallel processes")

    except ImportError:
        print("❌ mpi4py not installed")
        print("\n📦 To install MPI support:")
        print("\n   On Linux/Mac:")
        print("     sudo apt-get install libopenmpi-dev  # Ubuntu/Debian")
        print("     brew install open-mpi               # macOS")
        print("     pip install mpi4py")
        print("\n   On Windows:")
        print("     1. Download MS-MPI: https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi")
        print("     2. Install MS-MPI SDK and Runtime")
        print("     3. pip install mpi4py")
        print("\n   Or use conda:")
        print("     conda install -c conda-forge mpi4py")


# Main benchmark runner
# =====================

if __name__ == "__main__":
    print("=" * 60)
    print("Parallelization Benchmarks for MD Simulation")
    print("=" * 60)
    
    print("\n1. NumPy Vectorization")
    print("-" * 60)
    benchmark_vectorization()
    
    if NUMBA_AVAILABLE:
        print("\n2. Numba JIT Compilation")
        print("-" * 60)
        benchmark_numba()
    
    print("\n3. Ensemble Parallelism")
    print("-" * 60)
    benchmark_ensemble()
    
    if TORCH_AVAILABLE:
        print("\n4. GPU Acceleration (PyTorch)")
        print("-" * 60)
        benchmark_gpu()

    print("\n5. MPI (Message Passing Interface)")
    print("-" * 60)
    show_mpi_info()

    print("\n" + "=" * 60)
    print("Benchmarks complete!")
    print("=" * 60)

