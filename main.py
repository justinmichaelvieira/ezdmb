"""Android deployment entry point; desktop startup remains ``python -m ezdmb``."""

import sys
from importlib import import_module
from pathlib import Path

source_directory = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(source_directory))

if __name__ == "__main__":
    import_module("ezdmb.android_entrypoint").main()
