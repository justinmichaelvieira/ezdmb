from os.path import dirname, join, abspath
from setuptools import setup, find_packages
from setuptools.command.sdist import sdist
from pyqt_distutils.build_ui import build_ui

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

setup(
    name='ezdmb',
    version='0.3',
    packages=find_packages(),
    url='https://github.com/justin',
    license='Lesser GPL v3',
    author='Justin Vieira',
    author_email='justin@rancorsoft.com',
    description='A dead-simple digital menu board configurator and display.',
    install_requires=REQS,
    python_requires=">=3.4",
    cmdclass=cmdclass
)
