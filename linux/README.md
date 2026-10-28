## Debian/Ubuntu installation

Build the Debian package from any working directory:

```bash
bash linux/debian/build-dpkg.sh
```

The package is written to `linux/python_package/ezdmb/resources/`. Install it
with `sudo apt install ./linux/python_package/ezdmb/resources/ezdmb_1.1.0_all.deb`;
APT will install the Python and PySide6 runtime dependencies. Launch the app
with `ezdmb` or from the desktop application menu.

Tagged GitHub releases also publish the generated `.deb` as a downloadable
release asset.
