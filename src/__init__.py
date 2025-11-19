"""
Two-Particle Molecular Dynamics Simulation Package

This package provides a simple 2D molecular dynamics simulation
of two particles interacting via the Lennard-Jones potential.
"""

from .md_simulation import Particle, LennardJonesPotential, TwoParticleMD

__all__ = ['Particle', 'LennardJonesPotential', 'TwoParticleMD']
__version__ = '1.0.0'

