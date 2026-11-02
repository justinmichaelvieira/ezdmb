## Debian/Ubuntu installation

Build the Debian package from any working directory:

```bash
bash linux/debian/build-dpkg.sh
```

The package is written to `linux/python_package/ezdmb/resources/`. Install it
and its runtime dependencies with:

```bash
bash debian/install.sh
```

The package requires Python 3.13 or later and the PySide6 Qt modules listed in
its Debian metadata. Debian 13 and recent Ubuntu releases provide these
packages; older distributions may not. APT resolves and installs the Python
and PySide6 dependencies. Launch the app with `ezdmb` or from the desktop
application menu.

Tagged GitHub releases also publish the generated `.deb` as a downloadable
release asset.
