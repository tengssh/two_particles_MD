# Quick Start Guide

## Running the Simulation

Simply run:
```bash
python -m src.md_simulation
```

Or from the src directory:
```bash
cd src
python md_simulation.py
```

## What Happens

### 1. **Initialization**
- Random seed is set to 42 (for reproducibility)
- Two particles are placed at random positions in a 20×20 Å box
- **Custom initial velocities** for each particle (configurable)
- Minimum separation of 2×σ (6.8 Å) is enforced to avoid extreme forces

### 2. **Simulation**
- Runs for 5000 time steps (5 picoseconds)
- Both particles move according to:
  - Lennard-Jones forces between them
  - Elastic collisions with box walls
  - Velocity Verlet integration algorithm

### 3. **Output**
Three plots are generated:

#### Plot 1: Trajectories
- Shows the 2D box with walls
- Blue line: Particle 1's path
- Red line: Particle 2's path
- Circles: Starting positions
- Squares: Ending positions

#### Plot 2: Energy
- Top panel: Kinetic, potential, and total energy vs time
- Bottom panel: Energy deviation (should be near zero)
- Tests simulation accuracy

#### Plot 3: Distance
- Inter-particle distance vs time
- Red dashed line: Equilibrium distance (3.81 Å)
- Shows if particles attract, repel, or orbit

## Customization

### Change Random Seed
```python
random_seed = 123  # Try different values
np.random.seed(random_seed)
```

### Change Initial Velocities
```python
# Set different velocities for each particle
velocity1 = np.array([0.01, 0.03])  # Particle 1
velocity2 = np.array([0.02, -0.01]) # Particle 2

# Or make both particles move with same velocity
velocity1 = np.array([0.02, 0.02])
velocity2 = np.array([0.02, 0.02])
```

### Change Box Size
```python
box_size = (30.0, 30.0)  # Larger box
```

### Change Simulation Time
```python
sim.run(n_steps=10000)  # Run for 10 picoseconds
```

### Change Time Step (for better energy conservation)
```python
sim = TwoParticleMD(
    particle1=particle1,
    particle2=particle2,
    potential=lj_potential,
    box_size=box_size,
    dt=0.1  # Smaller time step = better accuracy
)
```

## Understanding the Output

### Console Output Example
```
======================================================================
Two-Particle Molecular Dynamics Simulation in 2D Box
======================================================================
Random seed: 42
Particle 1 starting position: [7.99, 17.21]
Particle 2 starting position: [13.71, 11.58]
Initial separation: 8.03 Angstroms
Initial velocity (particle 1): [0.020, 0.020] A/fs
Starting 2D box simulation for 5000 steps (dt=1.0 fs)...
Total simulation time: 5000.000 fs
Box size: 20.0 x 20.0 Angstroms
Progress: 10%
...
Progress: 100%
Simulation complete!
Particle 1 wall collisions: 16
Particle 2 wall collisions: 6

Energy Statistics:
  Initial total energy: 0.026494 kcal/mol
  Final total energy:   -0.028268 kcal/mol
  Energy drift:         -5.476161e-02 kcal/mol
  Relative drift:       206.6942%
  [WARNING] Significant energy drift. Consider smaller time step.
```

### What to Look For

1. **Wall Collisions**: How many times each particle bounced off walls
2. **Energy Drift**: Should be < 1% for good accuracy
   - If drift is large, reduce `dt` (time step)
3. **Trajectories**: 
   - Do particles collide?
   - Do they orbit each other?
   - Do they escape to opposite corners?
4. **Distance Plot**:
   - Oscillations = bound system (particles orbit)
   - Increasing distance = unbound (particles escape)
   - Sharp dips = close encounters or collisions

## Interesting Experiments

### 1. Head-on Collision
```python
# Particles moving toward each other
pos1 = np.array([5.0, 10.0])
pos2 = np.array([15.0, 10.0])
vel1 = np.array([0.02, 0.0])
vel2 = np.array([-0.02, 0.0])
```

### 2. Parallel Motion
```python
# Same velocity, different y-positions
pos1 = np.array([5.0, 8.0])
pos2 = np.array([5.0, 12.0])
vel = np.array([0.02, 0.0])  # Both move right
```

### 3. High Energy
```python
# Fast particles
initial_velocity = np.array([0.05, 0.05])
```

### 4. Low Energy (Bound System)
```python
# Slow particles, close together
initial_velocity = np.array([0.005, 0.005])
# Start near equilibrium distance
```

## Troubleshooting

### Energy Drift Too Large
**Problem**: Energy drift > 10%
**Solution**: Reduce time step
```python
dt=0.1  # Instead of dt=1.0
```

### Particles Start Too Close
**Problem**: Huge forces, simulation explodes
**Solution**: Code automatically ensures minimum separation of 2×σ

### Plots Don't Show
**Problem**: Matplotlib backend issue
**Solution**: Add at start of script:
```python
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'
```

### Simulation Too Slow
**Problem**: Taking too long
**Solution**: Reduce steps or increase record_interval
```python
sim.run(n_steps=1000, record_interval=10)  # Record every 10 steps
```

### Unicode Encoding Error on Windows
**Problem**: `UnicodeEncodeError: 'cp950' codec can't encode character`
**Cause**: Windows console using non-UTF-8 encoding (CP950, CP936, etc.)
**Solution**: The code now automatically handles this! If you still see errors:

**Option 1: Set Environment Variable (Recommended)**
```bash
set PYTHONIOENCODING=utf-8
python -m src.md_simulation
```

**Option 2: Change Console Code Page**
```bash
chcp 65001
python -m src.md_simulation
```

**Option 3: Use PowerShell Instead of CMD**
PowerShell has better Unicode support than Command Prompt.

**Option 4: Run in Python IDE**
Most IDEs (VS Code, PyCharm, Jupyter) handle UTF-8 automatically.

**Technical Details:**
The code includes automatic encoding fixes for Windows:
```python
# Already included in src/md_simulation.py
# Only applies when running directly (not during tests)
if sys.platform == 'win32' and 'pytest' not in sys.modules:
    import io
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
```

This ensures all output uses UTF-8 encoding, preventing crashes from Unicode characters.
The fix is automatically disabled during testing to avoid interfering with pytest.

