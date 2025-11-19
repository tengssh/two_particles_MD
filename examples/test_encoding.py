#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick test to verify encoding fix works without breaking tests
"""

import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")
print(f"stdout encoding: {sys.stdout.encoding}")
print(f"stderr encoding: {sys.stderr.encoding}")
print(f"pytest in modules: {'pytest' in sys.modules}")

# Import the module
from src.md_simulation import Particle, LennardJonesPotential, TwoParticleMD
import numpy as np

print("\n" + "="*70)
print("Testing basic functionality...")
print("="*70)

# Create simple simulation
particle1 = Particle(
    position=np.array([5.0, 5.0]), 
    velocity=np.array([0.1, 0.0]), 
    is_fixed=True
)
particle2 = Particle(
    position=np.array([8.0, 5.0]), 
    velocity=np.array([-0.05, 0.0])
)
potential = LennardJonesPotential()
sim = TwoParticleMD(particle1, particle2, potential, box_size=(20.0, 20.0))

print(f"Created simulation: {sim}")
print(f"Initial energy: {sim.get_energies()}")

# Run a few steps
sim.run(10, record_interval=5)
print(f"After 10 steps: {sim.get_energies()}")

print("\n" + "="*70)
print("SUCCESS! No encoding errors.")
print("="*70)

