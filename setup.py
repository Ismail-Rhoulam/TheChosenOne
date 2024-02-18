from setuptools import setup, find_packages

setup(
    name='TheChosenOne',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='TheChosenOne is a Python library for fun.',
    long_description=open('README.md').read(),
    install_requires=['numpy'],
    url='https://github.com/Ismail-Rhoulam/TheChosenOne',
    author='Ismail RHOULAM',
    author_email='rhoulamismail@gmail.com'
)