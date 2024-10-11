from __future__ import annotations

import nox


@nox.session(reuse_venv=True)
def lint(session: nox.Session) -> None:
    """Run pre-commit hooks for linting."""
    session.install('pre-commit')
    session.run('pre-commit', 'run', '--all-files')


@nox.session(python=['3.8', '3.9', '3.10', '3.11', '3.12', '3.13'], reuse_venv=True)
def test(session: nox.Session) -> None:
    """Run tests."""
    session.install('.')
    session.install('-r', 'requirements-dev.txt')
    session.run('coverage', 'erase')
    session.run('coverage', 'run', '-m', 'pytest', 'tests', *session.posargs)
    session.run('coverage', 'report')


@nox.session()
def build(session: nox.Session) -> None:
    """Build the package for distribution."""
    session.install('build[virtualenv]')
    session.run('python', '-m', 'build')
