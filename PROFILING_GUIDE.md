# Performance Profiling Guide

This guide covers comprehensive performance profiling techniques for Python and molecular dynamics simulations.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Profiling Tools Overview](#profiling-tools-overview)
3. [Built-in Python Profilers](#built-in-python-profilers)
4. [Visual Profilers](#visual-profilers)
5. [GPU Profiling](#gpu-profiling)
6. [MPI Profiling](#mpi-profiling)
7. [System-Level Profiling](#system-level-profiling)
8. [Best Practices](#best-practices)
9. [Profiling Workflow](#profiling-workflow)

---

## 🚀 Quick Start

### Run the Example Profiling Script

```bash
# Basic profiling
python examples/profile_md.py

# With line profiler
kernprof -l -v examples/profile_md.py

# With memory profiler
python -m memory_profiler examples/profile_md.py
```

### Interactive Profiling in Jupyter

```bash
jupyter notebook examples/profiling_examples.ipynb
```

---

## 📊 Profiling Tools Overview

### Comparison Table

| Tool | Type | Overhead | Best For | Output Format |
|------|------|----------|----------|---------------|
| **cProfile** | Deterministic | 10-50% | Function-level profiling | Text table |
| **line_profiler** | Deterministic | 100-1000% | Line-by-line analysis | Text table |
| **memory_profiler** | Sampling | 10-100% | Memory usage tracking | Text table |
| **py-spy** | Sampling | 1-5% | Production profiling | Flame graph (SVG) |
| **pyinstrument** | Statistical | 5-20% | Call stack analysis | Tree/HTML |
| **timeit** | Manual | 0% | Micro-benchmarks | Numeric |
| **perf** (Linux) | Hardware | <1% | CPU performance counters | Flame graph |
| **nvprof/nsys** | Hardware | <5% | GPU profiling | Timeline/trace |

### When to Use Each Tool

- **Quick timing** → `time.perf_counter()` or `%timeit`
- **Find slow functions** → `cProfile` + `SnakeViz`
- **Find slow lines** → `line_profiler`
- **Memory leaks** → `memory_profiler` or `tracemalloc`
- **Production profiling** → `py-spy`
- **GPU bottlenecks** → `nvprof` or PyTorch Profiler
- **MPI communication** → `mpiP` or Scalasca

---

## 🔧 Built-in Python Profilers

### 1. cProfile (Standard Library)

**Best for:** Overall function-level profiling

#### Basic Usage

```python
import cProfile
import pstats

# Method 1: Profile a statement
cProfile.run('simulation.run(1000)', 'profile_stats.prof')

# Method 2: Profile a code block
profiler = cProfile.Profile()
profiler.enable()

# Your code here
simulation.run(1000)

profiler.disable()

# Analyze results
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')  # Sort by cumulative time
stats.print_stats(20)  # Show top 20 functions
```

#### Command Line Usage

```bash
# Profile script
python -m cProfile -o profile.prof md_simulation.py

# View results
python -m pstats profile.prof
# Then in pstats shell:
# sort cumulative
# stats 20
```

#### Understanding Output

```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1000    2.500    0.003    5.000    0.005 md_simulation.py:321(step)
     1000    1.500    0.002    1.500    0.002 md_simulation.py:369(get_energies)
```

- **ncalls**: Number of calls
- **tottime**: Total time spent in function (excluding subcalls)
- **percall**: tottime / ncalls
- **cumtime**: Cumulative time (including subcalls)
- **percall**: cumtime / ncalls

---

### 2. line_profiler

**Best for:** Line-by-line profiling of specific functions

#### Installation

```bash
pip install line_profiler
```

#### Usage

```python
from line_profiler import LineProfiler

def profile_function():
    lp = LineProfiler()
    lp.add_function(compute_forces)  # Add functions to profile
    lp.add_function(integrate_step)
    
    lp.enable()
    simulation.run(100)
    lp.disable()
    
    lp.print_stats()

# Or use decorator
@profile
def compute_forces(positions):
    # ... code ...
    pass
```

#### Command Line Usage

```bash
# Add @profile decorator to functions you want to profile
# Then run:
kernprof -l -v script.py
```

#### Understanding Output

```
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
   150      1000      50000     50.0      10.0      r = np.linalg.norm(r_vec)
   151      1000     200000    200.0      40.0      force = compute_lj(r)
   152      1000     250000    250.0      50.0      forces[i] += force
```

- **Hits**: Number of times line was executed
- **Time**: Total time spent on line (microseconds)
- **Per Hit**: Average time per execution
- **% Time**: Percentage of total time

---

### 3. memory_profiler

**Best for:** Memory usage tracking

#### Installation

```bash
pip install memory_profiler
```

#### Usage

```python
from memory_profiler import profile

@profile
def allocate_arrays(N):
    positions = np.zeros((N, 3))      # Allocates memory
    velocities = np.zeros((N, 3))     # More memory
    forces = np.zeros((N, 3))         # Even more
    return positions, velocities, forces
```

#### Command Line Usage

```bash
python -m memory_profiler script.py
```

#### Understanding Output

```
Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
     5     50.0 MiB     50.0 MiB            1   positions = np.zeros((N, 3))
     6     75.0 MiB     25.0 MiB            1   velocities = np.zeros((N, 3))
     7    100.0 MiB     25.0 MiB            1   forces = np.zeros((N, 3))
```

- **Mem usage**: Total memory used by Python process
- **Increment**: Memory added by this line
- **Occurrences**: Number of times line was executed

---

### 4. tracemalloc (Standard Library)

**Best for:** Finding memory leaks

```python
import tracemalloc

# Start tracing
tracemalloc.start()

# Your code
simulation.run(1000)

# Get memory snapshot
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

# Display top 10 memory allocations
print("[ Top 10 ]")
for stat in top_stats[:10]:
    print(stat)

tracemalloc.stop()
```

---

## 🎨 Visual Profilers

### 1. py-spy

**Best for:** Production profiling without code changes

#### Installation

```bash
pip install py-spy
```

#### Usage

```bash
# Profile running process
py-spy top --pid 12345

# Generate flame graph
py-spy record -o profile.svg -- python md_simulation.py

# Sample running process for 60 seconds
py-spy record --pid 12345 --duration 60 -o profile.svg

# Profile with native extensions
py-spy record --native -o profile.svg -- python md_simulation.py
```

#### Features

- ✅ No code modification required
- ✅ Very low overhead (~1%)
- ✅ Works on running processes
- ✅ Beautiful flame graphs
- ✅ Can profile C extensions

---

### 2. SnakeViz

**Best for:** Interactive cProfile visualization

#### Installation

```bash
pip install snakeviz
```

#### Usage

```bash
# Generate profile
python -m cProfile -o profile.prof md_simulation.py

# Visualize in browser
snakeviz profile.prof
```

#### Features

- ✅ Interactive sunburst/icicle charts
- ✅ Zoom into specific functions
- ✅ Filter by time/calls
- ✅ Export to various formats

---

### 3. pyinstrument

**Best for:** Statistical profiling with call stacks

#### Installation

```bash
pip install pyinstrument
```

#### Usage

```python
from pyinstrument import Profiler

profiler = Profiler()
profiler.start()

# Your code
simulation.run(1000)

profiler.stop()

# Print to console
print(profiler.output_text(unicode=True, color=True))

# Save HTML report
with open('profile.html', 'w') as f:
    f.write(profiler.output_html())

# Open in browser
profiler.open_in_browser()
```

#### Example Output

```
  _     ._   __/__   _ _  _  _ _/_   Recorded: 14:23:45  Samples:  1000
 /_//_/// /_\ / //_// / //_'/ //     Duration: 5.234     CPU time: 5.180
/   _/                      v4.0.3

5.234 run  md_simulation.py:413
└─ 3.500 step  md_simulation.py:321
   ├─ 2.000 _calculate_forces  md_simulation.py:252
   └─ 1.500 get_energies  md_simulation.py:369
```

---

## 🖥️ GPU Profiling

### 1. NVIDIA Nsight Systems

**Best for:** CUDA profiling and timeline analysis

#### Installation

Download from [NVIDIA Developer](https://developer.nvidia.com/nsight-systems)

#### Usage

```bash
# Profile Python script
nsys profile -o profile.qdrep python gpu_simulation.py

# Profile with CUDA API tracing
nsys profile --trace=cuda,nvtx -o profile.qdrep python gpu_simulation.py

# View in GUI
nsight-sys profile.qdrep
```

---

### 2. PyTorch Profiler

**Best for:** PyTorch-specific profiling

```python
import torch
from torch.profiler import profile, record_function, ProfilerActivity

with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    record_shapes=True,
    profile_memory=True,
    with_stack=True
) as prof:
    with record_function("model_inference"):
        output = model(input)

    with record_function("backward"):
        loss.backward()

# Print table
print(prof.key_averages().table(
    sort_by="cuda_time_total",
    row_limit=10
))

# Export for Chrome tracing
prof.export_chrome_trace("trace.json")

# Export for TensorBoard
prof.export_stacks("profiler_stacks.txt", "self_cuda_time_total")
```

---

### 3. CuPy Profiler

**Best for:** CuPy GPU profiling

```python
import cupy as cp

# Time range annotation
with cp.prof.time_range('force_calculation', color_id=0):
    forces = compute_forces_gpu(positions)

with cp.prof.time_range('integration', color_id=1):
    positions += velocities * dt

# Use nvprof or nsys to capture:
# nsys profile -o profile.qdrep python cupy_simulation.py
```

---

## 🌐 MPI Profiling

### 1. mpiP

**Best for:** MPI communication profiling

```bash
# Compile with mpiP
mpicc -o simulation simulation.c -lmpiP -lm -lunwind

# Run
mpiexec -n 4 ./simulation

# Generates mpiP report automatically
```

---

### 2. Scalasca

**Best for:** Large-scale MPI profiling

```bash
# Instrument
scalasca -instrument mpicc -o simulation simulation.c

# Run with analysis
scalasca -analyze mpiexec -n 1024 ./simulation

# Examine results
scalasca -examine scorep_*
```

---

### 3. TAU (Tuning and Analysis Utilities)

**Best for:** Comprehensive HPC profiling

```bash
# Profile MPI+OpenMP+CUDA
tau_exec -T mpi,openmp,cuda python mpi_simulation.py

# View results with ParaProf
paraprof
```

---

## 🖥️ System-Level Profiling

### 1. perf (Linux)

**Best for:** CPU performance counters

```bash
# Record profile with call graph
perf record -g python md_simulation.py

# View report
perf report

# Generate flame graph
perf script | stackcollapse-perf.pl | flamegraph.pl > perf.svg

# Profile specific events
perf stat -e cache-misses,cache-references python md_simulation.py
```

---

### 2. htop/top

**Best for:** Real-time resource monitoring

```bash
# Interactive process viewer
htop

# Monitor specific process
top -p 12345

# Batch mode (log to file)
top -b -n 10 -d 1 > cpu_usage.log
```

---

### 3. nvidia-smi

**Best for:** GPU monitoring

```bash
# Watch GPU usage (updates every second)
watch -n 1 nvidia-smi

# Log GPU metrics to CSV
nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.used,temperature.gpu \
           --format=csv -l 1 > gpu_log.csv

# Monitor specific GPU
nvidia-smi -i 0 --query-gpu=utilization.gpu --format=csv -l 1
```

---

## 📝 Best Practices

### Profiling Workflow

1. **Start broad** → Use `cProfile` to identify hot spots
2. **Zoom in** → Use `line_profiler` on slow functions
3. **Check memory** → Use `memory_profiler` if memory is an issue
4. **Visualize** → Use `py-spy` or `SnakeViz` for flame graphs
5. **Optimize** → Focus on top 20% of time-consuming code
6. **Verify** → Re-profile after optimization

### Common Pitfalls

❌ **Profiling debug builds** → Always profile optimized code
❌ **Too small samples** → Run enough iterations for statistical significance
❌ **Profiler overhead** → Some profilers add 10-100x overhead
❌ **Ignoring I/O** → Profile I/O separately from computation
❌ **Not profiling real data** → Use realistic problem sizes
❌ **Premature optimization** → Profile first, optimize later

### Tips for Accurate Profiling

✅ **Warm-up runs** → JIT compilers need warm-up (Numba, PyTorch)
✅ **Multiple runs** → Average over multiple runs for consistency
✅ **Disable turbo boost** → For reproducible CPU benchmarks
✅ **Close other apps** → Minimize background processes
✅ **Use production data** → Profile with realistic inputs
✅ **Profile hot paths** → Focus on frequently executed code

---

## 🔄 Profiling Workflow Example

### Step-by-Step Optimization

```python
# Step 1: Identify bottleneck with cProfile
import cProfile
cProfile.run('simulation.run(1000)', 'profile.prof')
# Result: step() takes 80% of time

# Step 2: Line-level profiling
from line_profiler import LineProfiler
lp = LineProfiler()
lp.add_function(simulation.step)
lp.run('simulation.run(100)')
# Result: Line 352 (force calculation) is slowest

# Step 3: Optimize the slow line
# Before: r = np.sqrt(np.sum((pos1 - pos2)**2))
# After:  r = np.linalg.norm(pos1 - pos2)  # 2x faster

# Step 4: Verify improvement
cProfile.run('simulation.run(1000)', 'profile_optimized.prof')
# Result: 40% speedup overall

# Step 5: Check memory usage
from memory_profiler import profile
@profile
def run_simulation():
    simulation.run(1000)
# Result: No memory leaks detected
```

---

## 📦 Recommended Profiling Stack

### Installation

```bash
# Add to requirements.txt or install directly
pip install line_profiler memory_profiler py-spy snakeviz pyinstrument
```

### requirements-profiling.txt

```txt
# Performance Profiling Tools
line_profiler>=3.0.0      # Line-by-line profiling
memory_profiler>=0.60.0   # Memory usage tracking
py-spy>=0.3.0             # Sampling profiler (flame graphs)
snakeviz>=2.1.0           # cProfile visualization
pyinstrument>=4.0.0       # Statistical profiler
psutil>=5.9.0             # System monitoring
```

---

## 🎯 Quick Reference

### Timing Snippets

```python
# Simple timing
import time
start = time.perf_counter()
# ... code ...
print(f"Elapsed: {time.perf_counter() - start:.4f}s")

# Context manager timing
from contextlib import contextmanager

@contextmanager
def timer(name):
    start = time.perf_counter()
    yield
    print(f"{name}: {time.perf_counter() - start:.4f}s")

with timer("Force calculation"):
    forces = compute_forces(positions)
```

### IPython/Jupyter Magic Commands

```python
# Time single line
%timeit positions + velocities * dt

# Time cell
%%timeit
forces = compute_forces(positions)
positions += velocities * dt

# Profile cell
%%prun
simulation.run(1000)

# Memory usage
%memit large_array = np.zeros((10000, 10000))
```

---

## 📚 Additional Resources

### Documentation

- [cProfile](https://docs.python.org/3/library/profile.html) - Python standard library
- [line_profiler](https://github.com/pyutils/line_profiler) - Line-by-line profiling
- [memory_profiler](https://github.com/pythonprofilers/memory_profiler) - Memory profiling
- [py-spy](https://github.com/benfred/py-spy) - Sampling profiler
- [pyinstrument](https://github.com/joerick/pyinstrument) - Statistical profiler

### Tutorials

- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
- [NumPy Performance](https://numpy.org/doc/stable/user/performance.html)
- [PyTorch Performance Tuning](https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html)

### Tools

- [Flame Graphs](http://www.brendangregg.com/flamegraphs.html) - Visualization technique
- [Chrome Tracing](https://www.chromium.org/developers/how-tos/trace-event-profiling-tool/) - Timeline viewer

---

## 🎓 Next Steps

1. **Run examples** → `python examples/profile_md.py`
2. **Try Jupyter notebook** → `jupyter notebook examples/profiling_examples.ipynb`
3. **Profile your code** → Apply techniques to your simulations
4. **Optimize** → Focus on bottlenecks identified by profiling
5. **Measure** → Always verify improvements with profiling

---

*This guide was created with Augment Agent assistance.*


