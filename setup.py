from setuptools import setup

GEN_version = '0.0.6'
READ_name = 'pacman-deck'

setup(
    name=READ_name,
    version=GEN_version,
    author='TPHRyan',
    url='https://github.com/TPHRyan/pacman-deck',
    license='MIT',
    description='A transparent approach to declarative package management in Arch.',
    long_description=open('README.md', 'r').read(),
    classifiers=[],
    py_modules=['pacman-deck'],
    entry_points={
        'console_scripts': [
            'deck=pacman-deck:main',
        ],
    },
)
