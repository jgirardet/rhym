import pathlib
import sys

__version__ = '0.1.0'

lib = pathlib.Path.home() / ".poetry" / "lib"
sys.path.insert(0, str(lib))

