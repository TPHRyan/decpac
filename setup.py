from setuptools import setup

setup(
    name="pacman-deck",
    version="0.0.6",
    author="TPHRyan",
    url="https://github.com/TPHRyan/pacman-deck",
    license="MIT",
    description="A transparent approach to declarative package management in Arch.",
    long_description=open("README.md", "r").read(),
    classifiers=[],
    py_modules=["pacdeck"],
    entry_points={"console_scripts": ["deck=pacdeck:main",],},
)
