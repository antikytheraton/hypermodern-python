"""Nox sessions."""
import tempfile

import nox
from nox.sessions import Session


nox.options.sessions = "lint", "mypy", "pytype", "tests"
locations = "src", "tests", "noxfile.py", "docs/conf.py"
package = "hypermodern_python"


@nox.session(python=["3.9"])
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=["3.9"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.run("poetry", "install", external=True)
    session.run("flake8", *args)


@nox.session(python=["3.9"])
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.run("poetry", "install", external=True)
    session.run("black", *args)


@nox.session(python=["3.9"])
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
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
    """Type-check using mypy."""
    args = session.posargs or locations
    session.run("poetry", "install", external=True)
    session.run("mypy", *args)


@nox.session(python=["3.9"])
def pytype(session: Session) -> None:
    """TType-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.run("poetry", "install", external=True)
    session.run("pytype", *args)


@nox.session(python=["3.9"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", f"--typeguard-packages={package}", *args, external=True)


@nox.session(python=["3.9"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", external=True)
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python=["3.9"])
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("poetry", "install", external=True)
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python=["3.9"])
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.run("poetry", "install", external=True)
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
