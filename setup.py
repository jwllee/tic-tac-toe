from glob import glob
from os.path import splitext, basename
from setuptools import find_packages, setup


with open('requirements.txt', 'r') as f:
    requirements = f.readlines()


VERSION = '0.1.0'


setup(
    name='tictac',
    version=VERSION,
    description='Tic tac toe package',
    author='Wai Lam Jonathan Lee',
    author_email='jonathan.wailam.lee@gmail.com',
    install_requires=requirements,
    packages=find_packages()
)

