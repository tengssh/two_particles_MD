# MPI Installation Guide

This guide covers installing MPI (Message Passing Interface) and mpi4py for distributed computing in molecular dynamics simulations.

## 📋 What is MPI?

**MPI (Message Passing Interface)** is a standardized communication protocol for parallel computing across multiple processors/nodes. It's the industry standard for HPC (High-Performance Computing) and enables:

- ✅ Scaling to 1000s of cores across multiple nodes
- ✅ Efficient inter-process communication
- ✅ Domain decomposition for large MD simulations
- ✅ Replica exchange and parallel tempering

## 🎯 When Do You Need MPI?

**You need MPI if:**
- ✅ Running simulations with N > 100,000 particles
- ✅ Have access to HPC cluster or supercomputer
- ✅ Need to scale beyond single node (>64 cores)
- ✅ Doing replica exchange MD or parallel tempering

**You DON'T need MPI if:**
- ❌ Running on single workstation with <64 cores
- ❌ Simulating small systems (N < 10,000)
- ❌ Just doing parameter sweeps (use multiprocessing instead)

## 🔧 Installation Instructions

### Linux (Ubuntu/Debian)

#### Option 1: OpenMPI (Recommended)
```bash
# Update package list
sudo apt-get update

# Install OpenMPI
sudo apt-get install -y libopenmpi-dev openmpi-bin

# Verify installation
mpiexec --version

# Install mpi4py
pip install mpi4py

# Test installation
mpiexec -n 4 python -c "from mpi4py import MPI; print(f'Hello from rank {MPI.COMM_WORLD.Get_rank()}')"
```

#### Option 2: MPICH
```bash
# Install MPICH
sudo apt-get install -y mpich

# Verify installation
mpiexec --version

# Install mpi4py
pip install mpi4py
```

### macOS

#### Using Homebrew (Recommended)
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install OpenMPI
brew install open-mpi

# Verify installation
mpiexec --version

# Install mpi4py
pip install mpi4py

# Test installation
mpiexec -n 4 python -c "from mpi4py import MPI; print(f'Hello from rank {MPI.COMM_WORLD.Get_rank()}')"
```

### Windows

#### Option 1: MS-MPI (Recommended for Windows)

**Step 1: Download MS-MPI**
- Go to: https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi
- Download both:
  - MS-MPI SDK (for development)
  - MS-MPI Runtime (for execution)

**Step 2: Install MS-MPI**
```powershell
# Run the installers (as Administrator)
# 1. Install msmpisdk.msi
# 2. Install msmpisetup.exe

# Verify installation
mpiexec -help
```

**Step 3: Install mpi4py**
```powershell
# Install mpi4py
pip install mpi4py

# Test installation
mpiexec -n 4 python -c "from mpi4py import MPI; print(f'Hello from rank {MPI.COMM_WORLD.Get_rank()}')"
```

#### Option 2: Using WSL2 (Windows Subsystem for Linux)
```bash
# Install WSL2 first, then follow Linux instructions
wsl --install
# Restart computer
# Open WSL2 terminal and follow Ubuntu instructions above
```

### Using Conda (All Platforms)

```bash
# Create new environment with MPI support
conda create -n md_mpi python=3.11
conda activate md_mpi

# Install mpi4py (includes MPI)
conda install -c conda-forge mpi4py

# Verify installation
mpiexec --version
python -c "from mpi4py import MPI; print(MPI.Get_version())"
```

## ✅ Verification

### Test 1: Check MPI Installation
```bash
# Should show version info
mpiexec --version
```

### Test 2: Check mpi4py Installation
```python
python -c "from mpi4py import MPI; print(f'MPI Version: {MPI.Get_version()}')"
```

### Test 3: Run Simple MPI Program
```bash
# Create test file
cat > mpi_test.py << 'EOF'
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print(f"Hello from rank {rank} of {size} processes")
EOF

# Run with 4 processes
mpiexec -n 4 python mpi_test.py
```

**Expected output:**
```
Hello from rank 0 of 4 processes
Hello from rank 1 of 4 processes
Hello from rank 2 of 4 processes
Hello from rank 3 of 4 processes
```

## 🚀 Running MPI Programs

### Basic Usage
```bash
# Run on local machine with N processes
mpiexec -n 4 python my_mpi_script.py

# Specify number of processes per node
mpiexec -n 8 -ppn 4 python my_mpi_script.py  # 8 total, 4 per node
```

### Cluster Usage

#### With Hostfile
```bash
# Create hostfile
cat > hosts.txt << EOF
node1 slots=8
node2 slots=8
node3 slots=8
EOF

# Run across nodes
mpiexec -n 24 -hostfile hosts.txt python my_mpi_script.py
```

#### With SLURM
```bash
# Submit SLURM job
srun -n 64 -N 4 python my_mpi_script.py  # 64 processes on 4 nodes
```

#### With PBS/Torque
```bash
# Submit PBS job
mpiexec -n 32 python my_mpi_script.py
```

## 🐛 Troubleshooting

### Issue: "mpiexec: command not found"
**Solution:** MPI not installed or not in PATH
```bash
# Linux/Mac: Add to PATH
export PATH=/usr/local/bin:$PATH

# Or reinstall MPI
```

### Issue: "ImportError: No module named 'mpi4py'"
**Solution:** mpi4py not installed
```bash
pip install mpi4py
```

### Issue: "MPI_Init failed"
**Solution:** MPI runtime not properly configured
```bash
# Reinstall MPI
# Linux:
sudo apt-get install --reinstall libopenmpi-dev openmpi-bin

# Mac:
brew reinstall open-mpi
```

### Issue: Processes hang or don't communicate
**Solution:** Firewall blocking MPI communication
```bash
# Linux: Allow MPI ports
sudo ufw allow from 192.168.0.0/16  # Adjust for your network

# Or disable firewall temporarily for testing
sudo ufw disable
```

## 📚 Additional Resources

- **mpi4py Documentation**: https://mpi4py.readthedocs.io/
- **MPI Tutorial**: https://mpitutorial.com/
- **OpenMPI Documentation**: https://www.open-mpi.org/doc/
- **MS-MPI Documentation**: https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi

---

*This guide was created with Augment Agent assistance.*  
*Last Updated: 2024-11-08*

