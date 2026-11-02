# Debian/Ubuntu installation

From the repository root, build and install the package:

```bash
bash linux/debian/build-dpkg.sh
bash debian/install.sh
```

The install script uses APT to resolve the package's Python and PySide6
dependencies. The package requires Python 3.13 or later and the PySide6 Qt
modules declared in `linux/debian/DEBIAN/control`.