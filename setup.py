from setuptools import setup
from setuptools.command.build_py import build_py

from pyqt_distutils.build_ui import build_ui

class custom_build_py(build_py):
    def run(self):
        self.run_command('build_ui')
        build_py.run(self)

setup(
    name='ezdmb',
    version='0.1',
    packages=[],
    url='',
    license='',
    author='justin vieira',
    author_email='justin@rancorsoft.com',
    description='',
    cmdclass={
        'build_ui': build_ui,
        'build_py': custom_build_py,
    }
)