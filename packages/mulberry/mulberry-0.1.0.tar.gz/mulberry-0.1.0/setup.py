import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read().strip()

setuptools.setup(
    name="mulberry",
    version=version,
    author="Hunter Damron",
    author_email="hdamron1594@yahoo.com",
    description="Coordinate transformation tree with a focus on efficiency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hdamron17/mulberry",
    packages=["mulberry"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
    ],
)
