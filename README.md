Listing ZFS datasets as a tree
==============================

Development instructions:
-------------------------

Use `nox` to lint the codebase, set up a virtual environment together with an
installation of `flit`, then use `flit` to fetch the dependencies. The
executable the is in `.nox/install/bin/zfs-tree`. An invocation of `nox`
takes care of all that.

The generated executable will list the zfs datasets hierarchically in a
parent/child dependency tree.