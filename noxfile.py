import tempfile

import nox

nox.options.sessions = "lint", "safety", "tests"

locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.9"])
def tests(session: nox.Session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=["3.9"])
def lint(session: nox.Session):
    args = session.posargs or locations
    session.run("poetry", "install", external=True)
    session.run("flake8", *args)


@nox.session(python=["3.9"])
def black(session: nox.Session):
    args = session.posargs or locations
    session.run("poetry", "install", external=True)
    session.run("black", *args)


@nox.session(python=["3.9"])
def safety(session: nox.Session):
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
