import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyprimer",
    version="0.1.0",
    packages=["pyprimer"],
    python_requires=">=3.6",
    author="Manan (mentix02)",
    long_description=long_description,
    author_email="manan.yadav02@gmail.com",
    url="https://github.com/mentix02/pyprimer",
    long_description_content_type="text/markdown",
    description="A simple collection of prime number related functions.",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
