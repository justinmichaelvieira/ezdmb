from os.path import dirname, join, abspath
from setuptools import setup, find_packages
from setuptools.command.sdist import sdist
from pyqt_distutils.build_ui import build_ui
from src.ezdmb import version

CURDIR = dirname(abspath(__file__))
with open(join(CURDIR, "requirements.txt")) as rs:
    REQS = rs.read().splitlines()

cmdclass = {}


class custom_s_dist(sdist):
    def run(self):
        self.run_command('build_ui')
        super().run()


cmdclass["sdist"] = custom_s_dist


class custom_build_ui(build_ui):
    def run(self):
        build_ui.run(self)


cmdclass["build_ui"] = custom_build_ui

with open(join(CURDIR, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ezdmb',
    version=version,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justinmichaelvieira/ezdmb",
    project_urls={
        "Bug Tracker": "https://github.com/mahesh-maximus/helloworld-pyp/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: LGPL-3.0-only"
    ],
    package_dir={'':"src"},
    packages=find_packages("src"),
    license='GNU Lesser General Public License version 3',
    author='Justin Vieira',
    author_email='justin@rancorsoft.com',
    description='A dead-simple digital menu board configurator and display.',
    install_requires=REQS,
    python_requires=">=3.4",
    cmdclass=cmdclass,
    entry_points={
        "console_scripts": [
            "ezdmb = ezdmb.__main__:main"
        ]
    },
)
