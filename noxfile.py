import nox


@nox.session
def format(session):
    session.install("black")
    source_dirs = ["src"]
    session.run("black", *source_dirs)


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "--exclude", ".nox")


@nox.session
def install(session):
    session.install("flit")
    session.run("flit", "install", "--symlink", "--deps", "production")
