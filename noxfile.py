from __future__ import annotations

import nox


@nox.session(reuse_venv=True)
def lint(session: nox.Session) -> None:
    """Run pre-commit hooks for linting."""
    session.install('pre-commit')
    session.run('pre-commit', 'run', '--all-files')


@nox.session(reuse_venv=True)
def test(session: nox.Session) -> None:
    """Run tests."""
    session.install('tox')
    session.run('tox', 'run-parallel', '--', *session.posargs)


@nox.session()
def build(session: nox.Session) -> None:
    """Build the package for distribution."""
    session.install('build[virtualenv]')
    session.run('python', '-m', 'build')
