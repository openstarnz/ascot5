"""Modifies ascot2py.py so that it loads the libascot.so that setup.py compiles
and bundles in a5py/ascotpy/.libs/ when a5py is installed.
"""
import fileinput
import sys

for line in fileinput.input("src/ascot2py.py", inplace=True):
    if line.strip() == "_libraries['libascot.so'] = ctypes.CDLL('libascot.so')":
        sys.stdout.write(
            "# libascot.so is compiled and bundled here when a5py is installed (setup.py)\n"
            "from pathlib import Path\n"
            "libpath = Path(__file__).absolute().parent / \".libs\" / \"libascot.so\"\n"
            "try:\n"
            "    _libraries['libascot.so'] = ctypes.CDLL(str(libpath))\n"
            "except OSError as error:\n"
            "    raise ImportError(\n"
            "        f\"{error}. Reinstall a5py to compile libascot.so.\") from error\n"
            "\n"
            )
    else:
        sys.stdout.write(line)
