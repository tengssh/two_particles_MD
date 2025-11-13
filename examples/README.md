# Parallelization Examples

This directory contains practical examples demonstrating various parallelization techniques for molecular dynamics simulations.

## 📁 Files

- **`parallel_examples.py`** - Runnable benchmarks comparing different parallelization approaches

## 🚀 Quick Start

### Basic Run
```bash
python examples/parallel_examples.py
```

### With Optional Dependencies
```bash
# Install optional packages for full benchmarks
pip install numba torch

# Run benchmarks
python examples/parallel_examples.py
```

## 📊 What Gets Benchmarked

### 1. NumPy Vectorization
Compares traditional Python loops vs NumPy vectorized operations.

**Expected output:**
```
Loop version: 2.5000s
Vectorized version: 0.0250s
Speedup: 100.0x
```

### 2. Numba JIT Compilation (requires `numba`)
Demonstrates Just-In-Time compilation with parallel execution.

**Expected output:**
```
Numba parallel force calculation: 0.5000s for 1000 particles
Time per iteration: 0.0500s
```

### 3. Ensemble Parallelism
Runs multiple simulations in parallel using multiprocessing.

**Expected output:**
```
Serial ensemble: 4.0000s
Parallel ensemble: 1.2000s
Speedup: 3.3x
```

### 4. GPU Acceleration (requires `torch` + CUDA)
Compares CPU vs GPU performance for large arrays.

**Expected output (with GPU):**
```
Using GPU: NVIDIA GeForce RTX 3080
CPU (NumPy): 0.8000s
GPU (PyTorch): 0.0200s
Speedup: 40.0x
```

### 5. MPI (Message Passing Interface) (requires `mpi4py` + MPI)
Creates an example MPI script and shows how to run it.

**Expected output:**
```
✅ mpi4py is installed!
   MPI Version: (3, 1)

📝 MPI example saved to: mpi_example.py

🚀 To run MPI example:
   mpiexec -n 4 python mpi_example.py
```

## 📦 Dependencies

### Required
- `numpy` (included in requirements.txt)

### Optional
- `numba` - For JIT compilation examples
- `torch` - For GPU acceleration examples
- `mpi4py` - For MPI distributed computing examples

### Install Optional Dependencies

#### Option 1: Edit requirements.txt and Install All
```bash
# 1. Open requirements.txt
# 2. Uncomment the packages you need
# 3. Install
pip install -r requirements.txt
```

#### Option 2: Selective Install
```bash
# Numba (CPU parallelization)
pip install numba

# PyTorch (GPU acceleration)
# CPU-only version:
pip install torch

# GPU version (CUDA 11.8):
pip install torch --index-url https://download.pytorch.org/whl/cu118

# GPU version (CUDA 12.1):
pip install torch --index-url https://download.pytorch.org/whl/cu121

# MPI (distributed computing) - Requires MPI installation first!
# See MPI installation instructions below
pip install mpi4py
```

#### MPI Installation

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install libopenmpi-dev openmpi-bin
pip install mpi4py
```

**macOS:**
```bash
brew install open-mpi
pip install mpi4py
```

**Windows:**
1. Download MS-MPI from: https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi
2. Install both MS-MPI SDK and MS-MPI Runtime
3. Install mpi4py:
```bash
pip install mpi4py
```

**Using Conda (All platforms):**
```bash
conda install -c conda-forge mpi4py
```

## 🎯 Use Cases

### When to Use Each Technique

**NumPy Vectorization:**
- ✅ Always use as baseline
- ✅ Easy to implement
- ✅ 10-100x speedup over loops
- ✅ No additional dependencies

**Numba JIT:**
- ✅ Complex loops that can't be vectorized
- ✅ Pairwise force calculations
- ✅ 10-100x speedup
- ✅ Requires `numba` package

**Ensemble Parallelism:**
- ✅ Parameter sweeps
- ✅ Multiple independent simulations
- ✅ Perfect scaling (Nx speedup with N cores)
- ✅ Built-in multiprocessing

**GPU Acceleration:**
- ✅ Very large systems (N > 10,000)
- ✅ Long simulations
- ✅ 50-500x speedup
- ✅ Requires GPU + PyTorch/CuPy

**MPI (Distributed):**
- ✅ Very large systems (N > 100,000)
- ✅ Multi-node clusters
- ✅ 10-1000x speedup (scales to 1000s of cores)
- ✅ Requires MPI installation + mpi4py
- ✅ Standard for HPC/supercomputers

## 💡 Tips

### Interpreting Results

**Speedup < 2x:**
- Overhead dominates
- Problem too small for parallelization
- Consider serial implementation

**Speedup 2-10x:**
- Good parallelization
- Typical for CPU multiprocessing
- Check if more cores help

**Speedup > 10x:**
- Excellent parallelization
- Typical for GPU or vectorization
- Problem well-suited for technique

### Common Issues

**Numba not working:**
```bash
# Make sure you have compatible NumPy version
pip install numba numpy==1.24.3
```

**GPU not detected:**
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Check GPU info
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

**MPI not working:**
```bash
# Check if MPI is installed
mpiexec --version

# Check if mpi4py is installed
python -c "from mpi4py import MPI; print(MPI.Get_version())"

# Test basic MPI
mpiexec -n 2 python -c "from mpi4py import MPI; print(f'Rank {MPI.COMM_WORLD.Get_rank()}')"
```

**Multiprocessing slower than serial:**
- Problem too small (overhead > benefit)
- Try larger problem sizes
- Reduce number of processes

## 🔬 Extending the Examples

### Add Your Own Benchmark

```python
def my_custom_benchmark():
    """Your custom parallelization technique."""
    # Setup
    N = 1000
    data = np.random.rand(N, 2)
    
    # Benchmark
    start = time.time()
    result = my_parallel_function(data)
    elapsed = time.time() - start
    
    print(f"My technique: {elapsed:.4f}s")

# Add to main
if __name__ == "__main__":
    print("\n5. My Custom Technique")
    print("-" * 60)
    my_custom_benchmark()
```

### Test with Different Problem Sizes

```python
# Modify N in the examples
N_values = [100, 1000, 10000, 100000]

for N in N_values:
    print(f"\nN = {N}")
    # Run benchmark with this N
```

## 📚 Related Documentation

- **[PARALLELIZATION_GUIDE.md](../PARALLELIZATION_GUIDE.md)** - Comprehensive guide to all techniques
- **[README.md](../README.md)** - Main project documentation
- **[TESTING.md](../TESTING.md)** - Testing guide

## 🎓 Learning Path

1. **Start here:** Run `parallel_examples.py` to see speedups
2. **Read:** [PARALLELIZATION_GUIDE.md](../PARALLELIZATION_GUIDE.md) for theory
3. **Experiment:** Modify examples with different problem sizes
4. **Apply:** Implement techniques in your own code
5. **Benchmark:** Always measure before and after

## ⚠️ Important Notes

- **Benchmarks vary by hardware** - Your results will differ
- **Warm-up is important** - JIT compilation happens on first run
- **Problem size matters** - Small problems don't benefit from parallelization
- **Overhead exists** - Data transfer, process creation, etc.

## 🤝 Contributing

Have a parallelization technique to add? See [CONTRIBUTING.md](../CONTRIBUTING.md)!

---

*These examples were created with Augment Agent assistance.*  
*Last Updated: 2024-11-08*

