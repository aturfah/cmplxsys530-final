"""Script to upgrade all pip-installed packages."""

from subprocess import call
import pkg_resources


def upgrade_packages(wrk_set):
    """Call to upgrade packages."""
    packages = [dist.project_name for dist in wrk_set]
    call("pip install --user --upgrade " + ' '.join(packages), shell=True)


if __name__ == "__main__":
    upgrade_packages(pkg_resources.working_set)
