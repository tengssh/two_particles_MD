# Streamlit Interactive MD Simulation App

## Overview

The Streamlit app provides an interactive web interface for running and visualizing two-particle molecular dynamics simulations. It offers real-time parameter adjustment, simulation execution, and comprehensive visualization tools.

## Features

### 🎛️ Interactive Parameter Controls

Configure all simulation parameters through an intuitive web interface:

**Lennard-Jones Potential:**
- Epsilon (ε): Energy scale in kcal/mol
- Sigma (σ): Length scale in Angstroms

**Simulation Box:**
- Box width and height in Angstroms
- Customizable rectangular simulation domain

**Time Integration:**
- Time step (dt) in femtoseconds
- Number of simulation steps
- Random seed for reproducibility
- Real-time total simulation time calculation

**Particle Properties:**
- Individual mass settings (amu)
- Custom initial velocities (vx, vy) for each particle
- Fixed particle option to create stationary targets

### 🚀 Simulation Execution

- **One-click simulation**: Run button starts the simulation
- **Progress tracking**: Real-time progress bar with step counter
- **Performance metrics**: Displays wall collision counts and energy statistics
- **Session state**: Results persist across interactions

### 📊 Visualization Tabs

The app provides two main visualization modes:

#### 1. Static Outputs Tab

**Particle Trajectories:**
- Complete trajectory paths for both particles
- Start positions marked with X symbols
- End positions marked with circles
- Color-coded paths (blue for particle 1, red for particle 2)
- Box boundaries clearly displayed

**Energy Analysis:**
- Kinetic energy evolution
- Potential energy evolution
- Total energy conservation tracking
- Energy deviation from initial state
- Dual-panel layout for comprehensive analysis

**Inter-particle Distance:**
- Distance vs time plot
- Equilibrium distance reference line
- Helps identify collision and interaction events

#### 2. Interactive Trajectory Tab

**Plotly Animation:**
- Frame-by-frame trajectory playback
- Growing path visualization
- Play/Pause controls
- Interactive slider for frame navigation
- Hover information for particle positions
- Optimized frame sampling for smooth playback

### 📈 Energy Metrics Display

After simulation completion, the app displays:
- Initial total energy
- Final total energy
- Absolute energy drift
- Relative energy drift percentage

## Running the App

### Using Make (Recommended)

```bash
# Install dependencies
make install

# Launch the app
make app
```

The app will open in your default browser at `http://localhost:8501`

### Using Streamlit Directly

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run src/streamlit_app.py
```

### Command Line Options

```bash
# Run on specific port
streamlit run src/streamlit_app.py --server.port 8502

# Run in headless mode (no browser)
streamlit run src/streamlit_app.py --server.headless true
```

## Usage Guide

### Basic Workflow

1. **Adjust Parameters**: Use the sidebar or parameter columns to set simulation parameters
2. **Set Random Seed**: Choose a seed for reproducible results
3. **Configure Particles**: Set masses, velocities, and fixed status
4. **Run Simulation**: Click "🚀 Run Simulation" button
5. **View Results**: Explore visualizations in the tabs below

### Tips for Best Results

**Energy Conservation:**
- Use smaller time steps (dt = 0.1-1.0 fs) for better conservation
- Monitor the energy drift percentage (should be < 1%)

**Visualization:**
- Use 100-1000 steps for quick previews
- Use 5000+ steps for detailed trajectory analysis
- Adjust box size to match your particle separation

**Performance:**
- Reduce steps for faster execution
- Use fixed particles to study scattering scenarios
- Adjust frame step in animation for smoother playback

## Testing

The Streamlit app includes comprehensive tests in `tests/test_streamlit_app.py`:

### Test Coverage

**App Loading Tests:**
- ✅ App loads without errors
- ✅ Title and UI elements present
- ✅ Run button exists

**Parameter Input Tests:**
- ✅ Number inputs for all parameters
- ✅ Default values (epsilon, sigma, etc.)
- ✅ Parameter modification
- ✅ Checkbox controls for fixed particles

**Simulation Execution Tests:**
- ✅ Run button click handling
- ✅ Simulation produces results
- ✅ Session state storage

**Visualization Tests:**
- ✅ Trajectory figure creation
- ✅ Energy figure creation
- ✅ Distance figure creation
- ✅ Plotly animated trajectory
- ✅ Empty history edge cases

### Running Tests

```bash
# Run all tests (including Streamlit tests)
make test

# Run only Streamlit tests
pytest tests/test_streamlit_app.py -v

# Run specific test class
pytest tests/test_streamlit_app.py::TestSimulationExecution -v
```

## CI/CD Testing

The app is tested across multiple platforms in GitHub Actions:

### Platform-Specific Configurations

**Linux (Ubuntu):**
- Standard pytest execution
- MPLBACKEND=Agg for headless matplotlib

**macOS:**
- MPLBACKEND=Agg to prevent display server crashes
- Handles Abort trap: 6 errors

**Windows:**
- matplotlib.use('Agg') at module level
- Automatic figure cleanup with pytest fixtures
- Prevents Windows fatal exception: 0x80000003

### Test Optimizations

**Timeout Handling:**
- Reduced simulation steps to 10 for fast execution
- Increased AppTest timeout to 10 seconds
- Ensures tests complete in CI environments

**Resource Cleanup:**
```python
@pytest.fixture(autouse=True)
def cleanup_matplotlib():
    """Ensure all matplotlib figures are closed after each test."""
    yield
    plt.close('all')
```

See [`.github/workflows/README.md`](../.github/workflows/README.md) for detailed CI/CD documentation.

## Architecture

### File Structure

```
src/
├── streamlit_app.py          # Main Streamlit application
└── md_simulation.py          # Core simulation engine

tests/
└── test_streamlit_app.py     # Streamlit app tests (17 tests)
```

### Key Functions

**Visualization Functions:**
- `create_trajectory_figure(sim)`: Static matplotlib trajectory plot
- `create_energy_figure(sim)`: Energy analysis plots
- `create_distance_figure(sim)`: Inter-particle distance plot
- `create_plotly_animated_trajectory(sim, frame_step)`: Interactive animation

**Main Function:**
- `main()`: Streamlit app entry point with UI layout

### Design Decisions

**Why Streamlit?**
- Rapid prototyping of interactive interfaces
- No HTML/CSS/JavaScript required
- Built-in state management
- Easy deployment options

**Why Both Static and Interactive Visualizations?**
- Static: Better for publication-quality figures
- Interactive: Better for exploration and presentations

**Why Matplotlib + Plotly?**
- Matplotlib: Familiar to scientists, publication-ready
- Plotly: Interactive features, smooth animations

## Deployment

### Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy `src/streamlit_app.py`

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
EXPOSE 8501
CMD ["streamlit", "run", "src/streamlit_app.py"]
```

### Heroku

```bash
# Create Procfile
echo "web: streamlit run src/streamlit_app.py --server.port $PORT" > Procfile

# Deploy
heroku create
git push heroku main
```

## Troubleshooting

### Common Issues

**App won't start:**
- Check Python version (3.9+)
- Verify all dependencies installed
- Check for port conflicts

**Plots not displaying:**
- Ensure matplotlib backend is set correctly
- Check browser console for errors
- Try clearing Streamlit cache

**Slow performance:**
- Reduce number of simulation steps
- Increase frame_step for animations
- Use smaller box sizes

**Memory issues:**
- Reduce simulation steps
- Clear session state between runs
- Close unused browser tabs

## Future Enhancements

Potential improvements:
- [ ] Real-time animation during simulation
- [ ] Export results to CSV/JSON
- [ ] Parameter presets for common scenarios
- [ ] 3D visualization option
- [ ] Multi-particle support (N-body)
- [ ] Temperature control (thermostat)
- [ ] Comparison mode for multiple simulations

## References

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Testing Guide](https://docs.streamlit.io/develop/api-reference/app-testing)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
