# Parallelization Techniques for MD Simulation

This guide explores various parallelization strategies applicable to this molecular dynamics simulation project, from the current 2-particle system to potential N-body extensions.

## 📊 Current Project Analysis

### Computational Bottlenecks

**Current 2-Particle System:**
- ✅ **Very fast** - No parallelization needed for 2 particles
- Main loop: `O(n_steps)` - inherently sequential (time evolution)
- Force calculation: `O(1)` - single pairwise interaction
- Wall collisions: `O(1)` - two particles to check

**Scaling to N Particles:**
- Force calculation: `O(N²)` - all pairwise interactions
- Wall collisions: `O(N)` - check each particle
- History recording: `O(N)` - store N particle states

### Parallelizable Components

| Component | Current Complexity | Parallelizable? | Technique |
|-----------|-------------------|-----------------|-----------|
| Force calculation | O(1) | ✅ Yes (for N>2) | Spatial decomposition |
| Wall collisions | O(1) | ✅ Yes (for N>2) | Data parallelism |
| Position updates | O(1) | ✅ Yes (for N>2) | Data parallelism |
| Velocity updates | O(1) | ✅ Yes (for N>2) | Data parallelism |
| Time stepping | O(n_steps) | ❌ No | Sequential dependency |
| History recording | O(1) | ⚠️ Maybe | Async I/O |

---

## 🚀 Parallelization Techniques

### 1. **Data Parallelism** (Best for N-body extension)

Parallelize operations across multiple particles.

#### Use Cases:
- Position updates for all particles
- Velocity updates for all particles
- Wall collision checks
- Energy calculations

#### Implementation Options:

**A. NumPy Vectorization** (Easiest, 2-10x speedup)
```python
# Current (loop-based)
for i in range(N):
    particles[i].position += particles[i].velocity * dt

# Vectorized (parallel on CPU)
positions += velocities * dt  # NumPy broadcasts automatically
```

**B. Numba JIT Compilation** (Medium difficulty, 10-100x speedup)
```python
from numba import jit, prange

@jit(nopython=True, parallel=True)
def update_positions_parallel(positions, velocities, dt, N):
    for i in prange(N):  # prange = parallel range
        positions[i] += velocities[i] * dt
    return positions
```

**C. Multiprocessing** (Complex, good for CPU-bound tasks)
```python
from multiprocessing import Pool

def update_particle_batch(particle_batch):
    # Update a subset of particles
    for p in particle_batch:
        p.position += p.velocity * dt
    return particle_batch

# Split particles into batches
with Pool(processes=4) as pool:
    results = pool.map(update_particle_batch, particle_batches)
```

---

### 2. **Spatial Decomposition** (For large N-body systems)

Divide simulation space into cells/domains.

#### Concept:
```
┌─────────┬─────────┬─────────┐
│ Cell 0  │ Cell 1  │ Cell 2  │  Each cell processed
│  (CPU0) │  (CPU1) │  (CPU2) │  by different thread
├─────────┼─────────┼─────────┤
│ Cell 3  │ Cell 4  │ Cell 5  │  Only compute forces
│  (CPU3) │  (CPU0) │  (CPU1) │  within cell + neighbors
├─────────┼─────────┼─────────┤
│ Cell 6  │ Cell 7  │ Cell 8  │
│  (CPU2) │  (CPU3) │  (CPU0) │
└─────────┴─────────┴─────────┘
```

#### Implementation:
```python
class SpatialGrid:
    def __init__(self, box_size, cell_size):
        self.cells = {}  # cell_id -> list of particles
        
    def assign_particles(self, particles):
        """Assign particles to cells based on position."""
        for p in particles:
            cell_id = self.get_cell_id(p.position)
            self.cells[cell_id].append(p)
    
    def compute_forces_parallel(self):
        """Compute forces in parallel for each cell."""
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.compute_cell_forces, cell_id)
                for cell_id in self.cells
            ]
            wait(futures)
```

**Advantages:**
- ✅ Reduces O(N²) to O(N) for force calculations
- ✅ Scales to millions of particles
- ✅ Used in production MD codes (LAMMPS, GROMACS)

---

### 3. **GPU Acceleration** (Massive parallelism)

Use GPU for highly parallel operations.

#### Best Libraries:

**A. CuPy** (NumPy-like GPU arrays)
```python
import cupy as cp

# Move data to GPU
positions_gpu = cp.array(positions)
velocities_gpu = cp.array(velocities)

# Compute on GPU (automatically parallel)
positions_gpu += velocities_gpu * dt

# Move back to CPU if needed
positions = cp.asnumpy(positions_gpu)
```

**B. PyTorch** (Deep learning framework, great for MD)
```python
import torch

# Use GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

positions = torch.tensor(positions, device=device)
velocities = torch.tensor(velocities, device=device)

# All operations run on GPU
positions += velocities * dt
```

**C. Custom CUDA Kernels** (Maximum performance)
```python
from numba import cuda

@cuda.jit
def update_positions_gpu(positions, velocities, dt):
    idx = cuda.grid(1)
    if idx < positions.shape[0]:
        positions[idx] += velocities[idx] * dt
```

**When to use GPU:**
- ✅ N > 10,000 particles
- ✅ Many force calculations
- ✅ Long simulations (millions of steps)
- ❌ Small systems (overhead > benefit)

---

### 4. **Task Parallelism** (Different operations in parallel)

Run independent tasks simultaneously.

#### Example: Parallel Analysis
```python
from concurrent.futures import ThreadPoolExecutor

def analyze_simulation(sim):
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Run these analyses in parallel
        future_energy = executor.submit(sim.plot_energy)
        future_traj = executor.submit(sim.plot_trajectory)
        future_dist = executor.submit(sim.plot_distance)
        
        # Wait for all to complete
        future_energy.result()
        future_traj.result()
        future_dist.result()
```

#### Use Cases:
- Parallel visualization generation
- Concurrent data analysis
- Multiple simulation runs with different parameters

---

### 5. **Ensemble Parallelism** (Multiple simulations)

Run multiple independent simulations in parallel.

#### Use Cases:
- Parameter sweeps (different temperatures, pressures)
- Statistical sampling (different initial conditions)
- Replica exchange MD

#### Implementation:
```python
from multiprocessing import Pool
import itertools

def run_simulation(params):
    """Run single simulation with given parameters."""
    temp, pressure = params
    sim = create_simulation(temperature=temp, pressure=pressure)
    sim.run(n_steps=10000)
    return sim.get_results()

# Parameter grid
temperatures = [100, 200, 300, 400, 500]
pressures = [1.0, 2.0, 3.0]
param_combinations = list(itertools.product(temperatures, pressures))

# Run all combinations in parallel
with Pool(processes=8) as pool:
    results = pool.map(run_simulation, param_combinations)
```

**Advantages:**
- ✅ Perfect scaling (no communication overhead)
- ✅ Easy to implement
- ✅ Great for parameter studies

---

### 6. **Asynchronous I/O** (Non-blocking data operations)

Don't wait for I/O operations to complete.

#### Example: Async History Recording
```python
import asyncio
import aiofiles

class AsyncMD(TwoParticleMD):
    async def _record_state_async(self):
        """Record state without blocking simulation."""
        async with aiofiles.open('trajectory.dat', 'a') as f:
            await f.write(f"{self.time},{self.particle1.position}\n")

    def run_async(self, n_steps):
        """Run simulation with async I/O."""
        for step in range(n_steps):
            self.step()
            # Don't wait for write to complete
            asyncio.create_task(self._record_state_async())
```

---

### 7. **MPI (Message Passing Interface)** (Distributed computing)

Scale across multiple nodes in a cluster using MPI for inter-process communication.

#### Concept:
MPI allows multiple processes (potentially on different machines) to communicate and coordinate work. Perfect for HPC clusters.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Node 1    │     │   Node 2    │     │   Node 3    │
│  (Rank 0)   │────▶│  (Rank 1)   │────▶│  (Rank 2)   │
│ 1000 atoms  │     │ 1000 atoms  │     │ 1000 atoms  │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
              MPI_Allreduce (gather forces)
```

#### Use Cases:
- **Domain decomposition**: Each rank handles a spatial region
- **Replica exchange MD**: Each rank runs different temperature
- **Force calculation**: Distribute pairwise calculations
- **Large-scale simulations**: 1000s of cores across cluster

#### Implementation with mpi4py:

**A. Basic MPI Setup**
```python
from mpi4py import MPI
import numpy as np

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Process ID (0, 1, 2, ...)
size = comm.Get_size()  # Total number of processes

print(f"Hello from rank {rank} of {size}")
```

**B. Domain Decomposition MD**
```python
from mpi4py import MPI
import numpy as np

class MPIMDSimulation:
    """MPI-parallelized MD simulation with domain decomposition."""

    def __init__(self, total_particles, box_size):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()

        # Divide particles among processes
        self.n_local = total_particles // self.size
        self.box_size = box_size

        # Each rank gets a spatial domain
        self.domain_bounds = self._compute_domain_bounds()

        # Initialize local particles
        self.local_positions = self._initialize_local_particles()
        self.local_velocities = np.random.randn(self.n_local, 3) * 0.1
        self.local_forces = np.zeros((self.n_local, 3))

    def _compute_domain_bounds(self):
        """Divide simulation box among ranks."""
        # Simple 1D decomposition along x-axis
        width = self.box_size[0] / self.size
        x_min = self.rank * width
        x_max = (self.rank + 1) * width
        return (x_min, x_max)

    def _initialize_local_particles(self):
        """Initialize particles in this rank's domain."""
        x_min, x_max = self.domain_bounds
        positions = np.random.rand(self.n_local, 3)
        positions[:, 0] = positions[:, 0] * (x_max - x_min) + x_min
        positions[:, 1] *= self.box_size[1]
        positions[:, 2] *= self.box_size[2]
        return positions

    def compute_forces(self):
        """Compute forces with ghost particle communication."""
        # Reset forces
        self.local_forces[:] = 0.0

        # 1. Identify particles near domain boundaries (need ghost particles)
        ghost_particles = self._get_boundary_particles()

        # 2. Exchange ghost particles with neighbors
        left_rank = (self.rank - 1) % self.size
        right_rank = (self.rank + 1) % self.size

        # Send to right, receive from left
        ghost_from_left = self.comm.sendrecv(
            ghost_particles, dest=right_rank, source=left_rank
        )

        # Send to left, receive from right
        ghost_from_right = self.comm.sendrecv(
            ghost_particles, dest=left_rank, source=right_rank
        )

        # 3. Compute local forces (including ghost interactions)
        self._compute_local_forces(ghost_from_left, ghost_from_right)

    def _compute_local_forces(self, ghost_left, ghost_right):
        """Compute forces between local and ghost particles."""
        # Local-local interactions
        for i in range(self.n_local):
            for j in range(i+1, self.n_local):
                r_vec = self.local_positions[i] - self.local_positions[j]
                f = self._lj_force(r_vec)
                self.local_forces[i] += f
                self.local_forces[j] -= f

        # Local-ghost interactions
        for i in range(self.n_local):
            for ghost_pos in ghost_left:
                r_vec = self.local_positions[i] - ghost_pos
                f = self._lj_force(r_vec)
                self.local_forces[i] += f

            for ghost_pos in ghost_right:
                r_vec = self.local_positions[i] - ghost_pos
                f = self._lj_force(r_vec)
                self.local_forces[i] += f

    def _lj_force(self, r_vec, epsilon=1.0, sigma=1.0):
        """Lennard-Jones force calculation."""
        r = np.linalg.norm(r_vec)
        if r < 1e-10:
            return np.zeros(3)
        sr6 = (sigma / r) ** 6
        force_mag = 24.0 * epsilon / r * (2.0 * sr6**2 - sr6)
        return force_mag * r_vec / r

    def step(self, dt):
        """Velocity Verlet integration step."""
        # Update positions
        accel = self.local_forces / 1.0  # mass = 1.0
        self.local_positions += self.local_velocities * dt + 0.5 * accel * dt**2

        # Handle particles that moved to other domains
        self._migrate_particles()

        # Compute new forces
        old_accel = accel.copy()
        self.compute_forces()
        new_accel = self.local_forces / 1.0

        # Update velocities
        self.local_velocities += 0.5 * (old_accel + new_accel) * dt

    def _migrate_particles(self):
        """Move particles that crossed domain boundaries."""
        x_min, x_max = self.domain_bounds

        # Find particles outside domain
        mask_left = self.local_positions[:, 0] < x_min
        mask_right = self.local_positions[:, 0] >= x_max

        # Send to neighbors
        left_rank = (self.rank - 1) % self.size
        right_rank = (self.rank + 1) % self.size

        # Exchange particles
        # (Implementation details omitted for brevity)
        pass

    def get_total_energy(self):
        """Compute total energy across all ranks."""
        # Compute local kinetic energy
        local_ke = 0.5 * np.sum(self.local_velocities**2)

        # Sum across all ranks
        total_ke = self.comm.allreduce(local_ke, op=MPI.SUM)

        return total_ke

    def run(self, n_steps, dt=0.001):
        """Run MPI-parallel simulation."""
        if self.rank == 0:
            print(f"Running MPI simulation with {self.size} processes")

        for step in range(n_steps):
            self.step(dt)

            if step % 100 == 0 and self.rank == 0:
                energy = self.get_total_energy()
                print(f"Step {step}: Total KE = {energy:.4f}")

        if self.rank == 0:
            print("Simulation complete!")

# Run the simulation
if __name__ == "__main__":
    sim = MPIMDSimulation(total_particles=10000, box_size=(20.0, 20.0, 20.0))
    sim.run(n_steps=1000)
```

**C. Replica Exchange MD (Temperature Parallel Tempering)**
```python
from mpi4py import MPI
import numpy as np

class ReplicaExchangeMD:
    """Each MPI rank runs a different temperature."""

    def __init__(self, base_temp, n_replicas):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()

        # Each rank has different temperature
        self.temperature = base_temp * (1.1 ** self.rank)

        # Initialize simulation at this temperature
        self.sim = self._create_simulation(self.temperature)

        print(f"Rank {self.rank}: T = {self.temperature:.2f} K")

    def run_with_exchanges(self, n_steps, exchange_interval=100):
        """Run with periodic replica exchanges."""
        for step in range(n_steps):
            # Run MD at fixed temperature
            self.sim.step()

            # Attempt replica exchange
            if step % exchange_interval == 0:
                self._attempt_exchange()

    def _attempt_exchange(self):
        """Attempt to exchange configurations with neighbor."""
        # Only exchange between even-odd pairs
        if self.rank % 2 == 0 and self.rank + 1 < self.size:
            partner = self.rank + 1
            self._exchange_with(partner)
        elif self.rank % 2 == 1:
            partner = self.rank - 1
            self._exchange_with(partner)

    def _exchange_with(self, partner):
        """Exchange configurations with partner rank."""
        # Compute exchange probability (Metropolis criterion)
        my_energy = self.sim.get_potential_energy()

        # Exchange energies
        partner_energy = self.comm.sendrecv(
            my_energy, dest=partner, source=partner
        )

        # Compute acceptance probability
        beta1 = 1.0 / self.temperature
        partner_temp = self.comm.sendrecv(
            self.temperature, dest=partner, source=partner
        )
        beta2 = 1.0 / partner_temp

        delta = (beta2 - beta1) * (my_energy - partner_energy)
        accept_prob = min(1.0, np.exp(delta))

        # Decide whether to exchange
        if np.random.rand() < accept_prob:
            # Exchange configurations
            partner_config = self.comm.sendrecv(
                self.sim.get_configuration(), dest=partner, source=partner
            )
            self.sim.set_configuration(partner_config)

            if self.rank < partner:
                print(f"Exchange accepted: {self.rank} ↔ {partner}")
```

**D. Running MPI Programs**
```bash
# Single machine, 4 processes
mpiexec -n 4 python mpi_md_simulation.py

# Cluster with hostfile
mpiexec -n 16 -hostfile hosts.txt python mpi_md_simulation.py

# SLURM cluster
srun -n 64 python mpi_md_simulation.py
```

#### Advantages of MPI:
- ✅ Scales to 1000s of cores across multiple nodes
- ✅ Standard for HPC (supercomputers)
- ✅ Efficient inter-process communication
- ✅ Works with any cluster/supercomputer
- ✅ Can combine with OpenMP for hybrid parallelism

#### Challenges:
- ⚠️ Complex to implement (domain decomposition, ghost particles)
- ⚠️ Load balancing can be tricky
- ⚠️ Communication overhead for small systems
- ⚠️ Debugging is harder (multiple processes)

#### When to Use MPI:
- ✅ Very large systems (N > 100,000)
- ✅ Access to HPC cluster
- ✅ Need to scale beyond single node
- ✅ Replica exchange or parallel tempering
- ❌ Small systems (overhead > benefit)
- ❌ Single workstation (use multiprocessing instead)

---

## 📈 Performance Comparison

### Expected Speedups (N = 10,000 particles)

| Technique | Speedup | Difficulty | Best For |
|-----------|---------|------------|----------|
| NumPy vectorization | 2-10x | ⭐ Easy | Small-medium N |
| Numba JIT | 10-100x | ⭐⭐ Medium | CPU-bound |
| Multiprocessing | 2-8x | ⭐⭐⭐ Hard | Independent tasks |
| Spatial decomposition | 10-1000x | ⭐⭐⭐⭐ Very Hard | Large N |
| GPU (CuPy/PyTorch) | 50-500x | ⭐⭐⭐ Hard | Massive parallelism |
| Custom CUDA | 100-1000x | ⭐⭐⭐⭐⭐ Expert | Maximum performance |
| MPI (distributed) | 10-1000x | ⭐⭐⭐⭐⭐ Expert | HPC clusters |
| Ensemble parallelism | Nx | ⭐ Easy | Parameter studies |

### Scaling Characteristics

| Technique | Single Node | Multi-Node | Memory | Communication |
|-----------|-------------|------------|--------|---------------|
| NumPy/Numba | ✅ Excellent | ❌ No | Shared | None |
| Multiprocessing | ✅ Good | ❌ No | Shared | Pipes |
| GPU | ✅ Excellent | ⚠️ Limited | GPU only | PCIe |
| MPI | ✅ Good | ✅ Excellent | Distributed | Network |
| Ensemble | ✅ Perfect | ✅ Perfect | Independent | None |

---

## 🎯 Recommendations for This Project

### Current 2-Particle System
**Recommendation:** ❌ **No parallelization needed**
- Already fast enough (<1ms per step)
- Overhead would slow it down
- Focus on correctness and clarity

### Extension to N-Body (N = 100-1,000)
**Recommendation:** ✅ **NumPy vectorization + Numba**
```python
# Step 1: Vectorize with NumPy
positions = np.array([p.position for p in particles])
velocities = np.array([p.velocity for p in particles])

# Step 2: Add Numba for force calculations
@jit(nopython=True)
def compute_all_forces(positions, N):
    forces = np.zeros_like(positions)
    for i in range(N):
        for j in range(i+1, N):
            r_vec = positions[i] - positions[j]
            f = compute_lj_force(r_vec)
            forces[i] += f
            forces[j] -= f
    return forces
```

### Large-Scale (N > 10,000)
**Recommendation:** ✅ **GPU + Spatial Decomposition**
- Use PyTorch or CuPy for GPU arrays
- Implement cell lists for O(N) scaling
- Consider existing frameworks (OpenMM, HOOMD-blue)

### Very Large-Scale (N > 100,000) or Multi-Node
**Recommendation:** ✅ **MPI + Domain Decomposition**
- Essential for HPC clusters
- Combine with GPU for maximum performance
- Use existing frameworks (LAMMPS, GROMACS)
- Consider hybrid MPI+OpenMP

### Parameter Studies
**Recommendation:** ✅ **Ensemble Parallelism**
- Perfect for exploring phase space
- Easy to implement with multiprocessing (single node)
- Use MPI for cluster-wide parameter sweeps
- Linear scaling with number of CPUs

---

## 💻 Implementation Priority

### Phase 1: Extend to N particles (N < 1000)
1. ✅ Refactor to use NumPy arrays for positions/velocities
2. ✅ Vectorize position and velocity updates
3. ✅ Add Numba JIT to force calculations
4. ✅ Benchmark and profile

### Phase 2: Optimize for larger N (N < 10,000)
1. ✅ Implement spatial decomposition (cell lists)
2. ✅ Add neighbor lists for force calculations
3. ✅ Profile and optimize hotspots
4. ✅ Add parallel force computation with Numba prange

### Phase 3: GPU acceleration (N > 10,000)
1. ✅ Port to PyTorch/CuPy
2. ✅ Implement GPU kernels for forces
3. ✅ Optimize memory transfers
4. ✅ Benchmark GPU vs CPU

### Phase 4: Production features
1. ✅ Ensemble parallelism for parameter sweeps
2. ✅ Async I/O for trajectory writing
3. ✅ Distributed computing (MPI) for very large systems

---

## 📚 Resources

### Libraries
- **Numba**: https://numba.pydata.org/ (JIT compilation)
- **CuPy**: https://cupy.dev/ (GPU arrays)
- **PyTorch**: https://pytorch.org/ (GPU + autodiff)
- **mpi4py**: https://mpi4py.readthedocs.io/ (MPI for Python)
- **Dask**: https://dask.org/ (parallel NumPy)
- **Ray**: https://ray.io/ (distributed computing)

### MPI Resources
- **mpi4py Documentation**: https://mpi4py.readthedocs.io/
- **MPI Tutorial**: https://mpitutorial.com/
- **Open MPI**: https://www.open-mpi.org/
- **MPICH**: https://www.mpich.org/
- **Intel MPI**: https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html

### Existing MD Frameworks (with MPI support)
- **LAMMPS**: Classical MD (C++, Python interface, MPI)
- **GROMACS**: High-performance MD (MPI + GPU)
- **NAMD**: Scalable MD (MPI, GPU)
- **OpenMM**: GPU-accelerated MD (Python API, single node)
- **HOOMD-blue**: GPU MD for soft matter (MPI + GPU)

### Learning Resources
- "Understanding Molecular Simulation" by Frenkel & Smit
- "Computer Simulation of Liquids" by Allen & Tildesley
- "Parallel Programming with MPI" by Peter Pacheco
- "Using MPI" by Gropp, Lusk, and Skjellum
- NVIDIA CUDA Programming Guide
- Numba documentation on parallel computing

### HPC Resources
- **XSEDE**: https://www.xsede.org/ (US supercomputing resources)
- **NERSC**: https://www.nersc.gov/ (DOE supercomputing)
- **AWS ParallelCluster**: https://aws.amazon.com/hpc/parallelcluster/
- **Google Cloud HPC**: https://cloud.google.com/solutions/hpc

---

*This guide was created with Augment Agent assistance.*  
*Last Updated: 2024-11-08*

