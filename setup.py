from os.path import dirname, join, abspath
from setuptools import setup, find_packages

CURDIR = dirname(abspath(__file__))
with open(join(CURDIR, "requirements.txt")) as rs:
    REQS = rs.read().splitlines()

with open(join(CURDIR, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ezdmb',
    version="0.9.23",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justinmichaelvieira/ezdmb",
    project_urls={
        "Bug Tracker": "https://github.com/mahesh-maximus/helloworld-pyp/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    package_dir={'':"src"},
    packages=find_packages("src"),
    license='LGPL-3.0-only',
    author='Justin Vieira',
    author_email='justin@rancorsoft.com',
    description='A dead-simple digital menu board configurator and display.',
    install_requires=REQS,
    python_requires=">=3.4",
    entry_points={
        "console_scripts": [
            "ezdmb = ezdmb.__main__:main"
        ]
    },
)
