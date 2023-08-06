Toy utility to present ZFS datsets as a tree
============================================

Development instructions:
-------------------------

First, use nox to lint the codebase:
  - nox -s lint

Then, set up a virtual environment, together with an installation of the flit
build tool:
  - python -m venv venv
  - source venv/bin/activate.fish
  - pip install flit

Then, proceed to building the package in the local virtual environment:
  - flit install

You now may play with the generated executable:
  - mud-tree-python

When you're doing, get out of the virtual environment:
  - deactivate