import os
import sys
from pathlib import Path

# Add the python directory to PYTHONPATH
python_dir = str(Path(__file__).parent.parent / 'python')
if python_dir not in sys.path:
    sys.path.insert(0, python_dir)
