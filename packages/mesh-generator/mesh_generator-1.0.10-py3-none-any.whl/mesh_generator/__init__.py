"""Mesh Generator PSI

Create a 1D Mesh in Python.

Important subpackages:
src- mesh calculations.
bin- output .dat files, optimization, plotting.


Documentation: https://q.predsci.com/docs/mesh_generator/

"""
from mesh_generator import src
from mesh_generator import bin
from mesh_generator.src.mesh import Mesh
from mesh_generator.src.mesh_segment import MeshSegment
from mesh_generator.bin.call_psi_mesh_tool import create_psi_mesh
