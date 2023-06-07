import tempfile

import nox
from nox.sessions import Session


nox.options.sessions = "lint", "mypy", "pytype", "tests"
locations = "src", "tests", "noxfile.py"
package = "hypermodern_python"


@nox.session(python=["3.9"])
def tests(session: Session) -> None:
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=["3.9"])
def lint(session: Session) -> None:
    args = session.posargs or locations
    session.run("poetry", "install", external=True)
    session.run("flake8", *args)


@nox.session(python=["3.9"])
def black(session: Session) -> None:
    args = session.posargs or locations
    session.run("poetry", "install", external=True)
    session.run("black", *args)


@nox.session(python=["3.9"])
def safety(session: Session) -> None:
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--with",
            "dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.run("poetry", "install", external=True)
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=["3.9"])
def mypy(session: Session) -> None:
    args = session.posargs or locations
    session.run("poetry", "install", external=True)
    session.run("mypy", *args)


@nox.session(python=["3.9"])
def pytype(session: Session) -> None:
    """Run static type checker"""
    args = session.posargs or ["--disable=import-error", *locations]
    session.run("poetry", "install", external=True)
    session.run("pytype", *args)


@nox.session(python=["3.9"])
def typeguard(session: Session) -> None:
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--only", "main", external=True)
    session.run("pytest", f"--typeguard-packages={package}", *args)
