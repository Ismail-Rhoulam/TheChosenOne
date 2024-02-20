from setuptools import setup, find_packages

setup(
    name='TheChosenOne',
    version='0.0.01',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='TheChosenOne is a Python library for university tasks',
    long_description=open('README.md').read(),
    install_requires=['easyocr'],
    url='https://github.com/Ismail-Rhoulam/TheChosenOne',
    author='Ismail RHOULAM',
    author_email='rhoulamismail@gmail.com'
)