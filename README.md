Toy utility to present ZFS datsets as a tree
============================================

Development instructions:
-------------------------

Use 'nox' to lint the codebase, set up a virtual environment together with an installation of flit, then use flit to fetch the dependencies. The executable the is in .nox/install/bin/mud-tree-python.

The generated executable will list the zfs datasets hierarchically in a parent/child dependency tree.