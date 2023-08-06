from setuptools import setup, find_packages

setup(
    name='dustydata',
    version='0.0.7',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Data Science Package',
    long_description=open('README.md').read(),
    install_requires=['sklearn'],
    author='Dustin Stringer',
)
