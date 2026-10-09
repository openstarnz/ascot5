import os
import shutil
import subprocess
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.dist import Distribution

ROOT = Path(__file__).parent.absolute()


class BuildLibascot(build_py):
    """Compile libascot.so with make and ship it inside a5py/ascotpy."""

    def run(self):
        # Always rebuild from scratch; make reads flags (MPI, DIPOLE_FIX, ...)
        # from the environment.
        subprocess.check_call(["make", "clean"], cwd=ROOT)
        subprocess.check_call(
            ["make", "libascot", f"-j{os.cpu_count() or 1}"], cwd=ROOT)
        (ROOT / "a5py" / "ascotpy" / ".libs").mkdir(exist_ok=True)
        shutil.copy2(ROOT / "build" / "libascot.so",
                     ROOT / "a5py" / "ascotpy" / ".libs" / "libascot.so")
        super().run()


class BinaryDistribution(Distribution):
    # Bundled libascot.so makes the wheel platform specific.
    def has_ext_modules(self):
        return True


setup(
    cmdclass={"build_py": BuildLibascot},
    distclass=BinaryDistribution,
    package_data={"a5py.ascotpy": [".libs/libascot.so"]},
)
