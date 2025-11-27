"""
Unit tests for the Streamlit MD Simulation App.

Uses Streamlit's official testing framework (AppTest) to test the app
without running a browser.
"""
import pytest
import sys
import os
import numpy as np

# Add parent directory to path to import from src
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..'))
_src_dir = os.path.join(_project_root, 'src')

if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from streamlit.testing.v1 import AppTest

# Path to the streamlit app
APP_PATH = os.path.join(_src_dir, 'streamlit_app.py')


class TestAppLoads:
    """Tests that the app loads correctly."""
    
    def test_app_loads_without_errors(self):
        """Test that the app loads without throwing any exceptions."""
        at = AppTest.from_file(APP_PATH).run()
        assert not at.exception, f"App raised exception: {at.exception}"
    
    def test_app_has_title(self):
        """Test that the app displays a title."""
        at = AppTest.from_file(APP_PATH).run()
        # Check that markdown or title exists
        assert len(at.title) > 0 or len(at.markdown) > 0
    
    def test_app_has_run_button(self):
        """Test that the app has a Run Simulation button."""
        at = AppTest.from_file(APP_PATH).run()
        assert len(at.button) > 0, "App should have at least one button"


class TestParameterInputs:
    """Tests for parameter input widgets."""
    
    def test_number_inputs_exist(self):
        """Test that the app has number input widgets for parameters."""
        at = AppTest.from_file(APP_PATH).run()
        # There should be many number inputs for all the parameters
        assert len(at.number_input) >= 10, "App should have multiple number inputs for parameters"
    
    def test_epsilon_input(self):
        """Test epsilon (LJ potential) input."""
        at = AppTest.from_file(APP_PATH).run()
        # First number input should be epsilon with default 0.238
        epsilon_input = at.number_input[0]
        assert epsilon_input.value == pytest.approx(0.238, rel=1e-3)
    
    def test_sigma_input(self):
        """Test sigma (LJ potential) input."""
        at = AppTest.from_file(APP_PATH).run()
        # Second number input should be sigma with default 3.4
        sigma_input = at.number_input[1]
        assert sigma_input.value == pytest.approx(3.4, rel=1e-2)
    
    def test_modify_parameter_value(self):
        """Test that parameter values can be modified."""
        at = AppTest.from_file(APP_PATH).run()
        # Change epsilon to a new value
        at.number_input[0].set_value(0.5).run()
        assert at.number_input[0].value == pytest.approx(0.5, rel=1e-3)
    
    def test_checkboxes_exist(self):
        """Test that fixed particle checkboxes exist."""
        at = AppTest.from_file(APP_PATH).run()
        # Should have 2 checkboxes for fixed particles
        assert len(at.checkbox) >= 2, "App should have checkboxes for fixed particles"


class TestSimulationExecution:
    """Tests for running the simulation."""
    
    def test_run_button_click(self):
        """Test that clicking Run Simulation button doesn't cause errors."""
        at = AppTest.from_file(APP_PATH).run()
        # Find and click the Run Simulation button
        # Adjust n_steps to smaller value for faster test
        # number_input[5] is n_steps (based on UI order)
        at.number_input[5].set_value(10).run()  # Minimal steps for fast test
        
        # Click the run button (usually the first/only primary button)
        # Increase timeout to 10s for CI environment
        at.button[0].click().run(timeout=10)
        
        # Check no exceptions occurred
        assert not at.exception, f"Simulation raised exception: {at.exception}"
    
    def test_simulation_produces_results(self):
        """Test that running simulation produces visualizations."""
        at = AppTest.from_file(APP_PATH).run()
        
        # Set minimal steps for fast execution
        at.number_input[5].set_value(10).run()
        
        # Run simulation with increased timeout
        at.button[0].click().run(timeout=10)
        
        # After running, there should be tabs for visualization
        assert len(at.tabs) > 0 or 'simulation' in at.session_state
    
    def test_session_state_stores_simulation(self):
        """Test that simulation is stored in session state after running."""
        at = AppTest.from_file(APP_PATH).run()
        
        # Set minimal steps
        at.number_input[5].set_value(10).run()
        
        # Run simulation with increased timeout
        at.button[0].click().run(timeout=10)
        
        # Check session state
        assert 'simulation' in at.session_state, "Simulation should be stored in session_state"


class TestVisualizationFunctions:
    """Tests for visualization helper functions."""
    
    def test_create_trajectory_figure(self):
        """Test that trajectory figure can be created."""
        from src.streamlit_app import create_trajectory_figure
        from src.md_simulation import Particle, LennardJonesPotential, TwoParticleMD
        
        # Create a minimal simulation
        lj = LennardJonesPotential(epsilon=0.238, sigma=3.4)
        p1 = Particle(position=np.array([5.0, 10.0]), velocity=np.array([0.01, 0.0]), mass=39.948)
        p2 = Particle(position=np.array([15.0, 10.0]), velocity=np.array([0.0, 0.0]), mass=39.948, is_fixed=True)
        sim = TwoParticleMD(p1, p2, lj, box_size=(20.0, 20.0), dt=1.0)
        
        # Run a few steps
        for _ in range(10):
            sim.step()
            sim.history['pos1'].append(sim.particle1.position.copy())
            sim.history['pos2'].append(sim.particle2.position.copy())
        
        # Create figure
        fig = create_trajectory_figure(sim)
        assert fig is not None, "Trajectory figure should be created"
    
    def test_create_energy_figure(self):
        """Test that energy figure can be created."""
        from src.streamlit_app import create_energy_figure
        from src.md_simulation import Particle, LennardJonesPotential, TwoParticleMD
        
        # Create a minimal simulation
        lj = LennardJonesPotential(epsilon=0.238, sigma=3.4)
        p1 = Particle(position=np.array([5.0, 10.0]), velocity=np.array([0.01, 0.0]), mass=39.948)
        p2 = Particle(position=np.array([15.0, 10.0]), velocity=np.array([0.0, 0.0]), mass=39.948, is_fixed=True)
        sim = TwoParticleMD(p1, p2, lj, box_size=(20.0, 20.0), dt=1.0)
        
        # Run and record
        for _ in range(10):
            sim.step()
            sim.history['time'].append(sim.time)
            ke, pe, total = sim.get_energies()
            sim.history['kinetic'].append(ke)
            sim.history['potential'].append(pe)
            sim.history['total'].append(total)
        
        # Create figure
        fig = create_energy_figure(sim)
        assert fig is not None, "Energy figure should be created"

    def test_create_distance_figure(self):
        """Test that distance figure can be created."""
        from src.streamlit_app import create_distance_figure
        from src.md_simulation import Particle, LennardJonesPotential, TwoParticleMD

        # Create a minimal simulation
        lj = LennardJonesPotential(epsilon=0.238, sigma=3.4)
        p1 = Particle(position=np.array([5.0, 10.0]), velocity=np.array([0.01, 0.0]), mass=39.948)
        p2 = Particle(position=np.array([15.0, 10.0]), velocity=np.array([0.0, 0.0]), mass=39.948, is_fixed=True)
        sim = TwoParticleMD(p1, p2, lj, box_size=(20.0, 20.0), dt=1.0)

        # Run and record
        for _ in range(10):
            sim.step()
            sim.history['time'].append(sim.time)
            sim.history['pos1'].append(sim.particle1.position.copy())
            sim.history['pos2'].append(sim.particle2.position.copy())

        # Create figure
        fig = create_distance_figure(sim)
        assert fig is not None, "Distance figure should be created"

    def test_create_plotly_animated_trajectory(self):
        """Test that Plotly animated trajectory can be created."""
        from src.streamlit_app import create_plotly_animated_trajectory
        from src.md_simulation import Particle, LennardJonesPotential, TwoParticleMD

        # Create a minimal simulation
        lj = LennardJonesPotential(epsilon=0.238, sigma=3.4)
        p1 = Particle(position=np.array([5.0, 10.0]), velocity=np.array([0.01, 0.0]), mass=39.948)
        p2 = Particle(position=np.array([15.0, 10.0]), velocity=np.array([0.0, 0.0]), mass=39.948, is_fixed=True)
        sim = TwoParticleMD(p1, p2, lj, box_size=(20.0, 20.0), dt=1.0)

        # Run and record history
        sim.history['time'].append(sim.time)
        sim.history['pos1'].append(sim.particle1.position.copy())
        sim.history['pos2'].append(sim.particle2.position.copy())

        for _ in range(50):
            sim.step()
            sim.history['time'].append(sim.time)
            sim.history['pos1'].append(sim.particle1.position.copy())
            sim.history['pos2'].append(sim.particle2.position.copy())

        # Create Plotly figure with small frame step
        fig = create_plotly_animated_trajectory(sim, frame_step=5)
        assert fig is not None, "Plotly animated figure should be created"
        # Check that figure has frames for animation
        assert len(fig.frames) > 0, "Plotly figure should have animation frames"


class TestEmptyHistory:
    """Tests for edge cases with empty history."""

    def test_trajectory_figure_empty_history(self):
        """Test trajectory figure returns None for empty history."""
        from src.streamlit_app import create_trajectory_figure
        from src.md_simulation import Particle, LennardJonesPotential, TwoParticleMD

        lj = LennardJonesPotential(epsilon=0.238, sigma=3.4)
        p1 = Particle(position=np.array([5.0, 10.0]), velocity=np.array([0.01, 0.0]), mass=39.948)
        p2 = Particle(position=np.array([15.0, 10.0]), velocity=np.array([0.0, 0.0]), mass=39.948)
        sim = TwoParticleMD(p1, p2, lj, box_size=(20.0, 20.0), dt=1.0)

        # Don't run any steps - history is empty
        fig = create_trajectory_figure(sim)
        assert fig is None, "Should return None for empty history"

    def test_energy_figure_empty_history(self):
        """Test energy figure returns None for empty history."""
        from src.streamlit_app import create_energy_figure
        from src.md_simulation import Particle, LennardJonesPotential, TwoParticleMD

        lj = LennardJonesPotential(epsilon=0.238, sigma=3.4)
        p1 = Particle(position=np.array([5.0, 10.0]), velocity=np.array([0.01, 0.0]), mass=39.948)
        p2 = Particle(position=np.array([15.0, 10.0]), velocity=np.array([0.0, 0.0]), mass=39.948)
        sim = TwoParticleMD(p1, p2, lj, box_size=(20.0, 20.0), dt=1.0)

        # Don't run any steps - history is empty
        fig = create_energy_figure(sim)
        assert fig is None, "Should return None for empty history"

