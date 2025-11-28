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

### Live Demo

**🚀 [https://two-particles-md.streamlit.app/](https://two-particles-md.streamlit.app/)**

The app is currently deployed on Streamlit Community Cloud and is publicly accessible.

### Streamlit Community Cloud (Recommended - Free)

**Current Deployment**: This project is deployed using this method.

#### Prerequisites
- GitHub account
- Repository pushed to GitHub
- `requirements.txt` in repository root

#### Step-by-Step Deployment Guide

**1. Prepare Your Repository**

Ensure your repository has:
```
two_particles_MD/
├── src/
│   └── streamlit_app.py    # Main app file
├── requirements.txt         # Dependencies
└── README.md
```

**2. Sign Up for Streamlit Community Cloud**

- Go to [share.streamlit.io](https://share.streamlit.io)
- Click "Sign in with GitHub"
- Authorize Streamlit to access your GitHub account

**3. Deploy Your App**

- Click "New app" button
- Fill in the deployment form:
  - **Repository**: `tengssh/two_particles_MD` (or your username/repo)
  - **Branch**: `main`
  - **Main file path**: `src/streamlit_app.py`
  - **App URL** (optional): Choose a custom subdomain or use auto-generated
- Click "Deploy!"

**4. Wait for Deployment**

- Initial deployment takes 2-5 minutes
- You'll see a build log showing:
  - Installing dependencies
  - Starting the app
  - Health checks
- Once complete, your app will be live!

**5. Get Your App URL**

Your app will be available at:
- Auto-generated: `https://[username]-[repo-name]-[random].streamlit.app`
- Custom: `https://[your-custom-name].streamlit.app`

**Example**: `https://two-particles-md.streamlit.app/`

#### Managing Your Deployment

**App Settings:**
- Access via Streamlit Community Cloud dashboard
- Settings → "Manage app"
- Options:
  - Reboot app
  - Delete app
  - View logs
  - Update settings

**Automatic Updates:**
- App automatically redeploys when you push to GitHub
- Monitors the specified branch (`main`)
- Deployment triggered within 1-2 minutes of push

**Viewing Logs:**
- Click "Manage app" → "Logs"
- Real-time logs show:
  - User visits
  - Errors
  - Performance metrics

**Resource Limits (Free Tier):**
- 1 GB RAM
- 1 CPU core
- Unlimited apps (public)
- Community support

#### Troubleshooting Deployment

**Issue: App won't start**
- Check `requirements.txt` has all dependencies
- Verify `src/streamlit_app.py` path is correct
- Check logs for specific errors

**Issue: Dependencies fail to install**
- Ensure Python version compatibility (3.9-3.12)
- Check for conflicting package versions
- Try pinning specific versions in `requirements.txt`

**Issue: App is slow**
- Free tier has limited resources
- Reduce simulation steps for faster execution
- Consider caching with `@st.cache_data`

**Issue: App goes to sleep**
- Free tier apps sleep after inactivity
- First visit after sleep takes ~30 seconds to wake
- Upgrade to paid tier for always-on apps

### Alternative Deployment Options

#### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and Run:**
```bash
# Build image
docker build -t two-particles-md .

# Run container
docker run -p 8501:8501 two-particles-md

# Access at http://localhost:8501
```

#### Heroku Deployment

**Setup Files:**

`Procfile`:
```
web: streamlit run src/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

`runtime.txt`:
```
python-3.11.0
```

**Deploy:**
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create two-particles-md

# Deploy
git push heroku main

# Open app
heroku open
```

#### Railway Deployment

**Steps:**
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Streamlit
5. Set start command: `streamlit run src/streamlit_app.py`
6. Deploy!

**Advantages:**
- Free tier: 500 hours/month
- Automatic HTTPS
- Custom domains
- Environment variables

#### Render Deployment

**Steps:**
1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run src/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
5. Deploy

**Advantages:**
- Free tier available
- Auto-deploy from GitHub
- SSL certificates included

### Deployment Best Practices

**1. Environment Variables**
- Use Streamlit secrets for sensitive data
- Create `.streamlit/secrets.toml` locally (gitignored)
- Add secrets in Streamlit Cloud dashboard

**2. Performance Optimization**
- Use `@st.cache_data` for expensive computations
- Reduce default simulation steps
- Optimize frame sampling for animations

**3. Monitoring**
- Check logs regularly
- Monitor resource usage
- Track user feedback

**4. Updates**
- Test locally before pushing
- Use feature branches for major changes
- Monitor deployment logs after updates

**5. Security**
- Don't commit secrets to GitHub
- Use environment variables for API keys
- Keep dependencies updated

### Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Streamlit Cloud** | ✅ Unlimited public apps | $20/month | Streamlit apps |
| **Heroku** | ❌ (discontinued) | $7/month | General web apps |
| **Railway** | 500 hrs/month | $5/month | Modern deployments |
| **Render** | 750 hrs/month | $7/month | Full-stack apps |
| **Docker** | Self-hosted | Variable | Full control |

### Recommended: Streamlit Community Cloud

**Why we chose it:**
- ✅ **Free**: Unlimited public apps
- ✅ **Easy**: One-click deployment from GitHub
- ✅ **Automatic**: Auto-deploy on git push
- ✅ **Optimized**: Built specifically for Streamlit
- ✅ **Fast**: Quick cold starts
- ✅ **Reliable**: 99.9% uptime

**Current Status:**
- **URL**: [https://two-particles-md.streamlit.app/](https://two-particles-md.streamlit.app/)
- **Platform**: Streamlit Community Cloud
- **Status**: ✅ Active
- **Auto-deploy**: Enabled (from `main` branch)

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
