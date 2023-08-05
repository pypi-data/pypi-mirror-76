import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mpl_trajectory",
    version="1.0.0",
    author="Mark Pearson",
    #author_email="author@example.com",
    description="A small package for matplotlib to show movement of trajectories in the form of animations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hitthesurf/mpl_trajectory",
    license = "MIT",
    py_modules = ["mpl_trajectory"],
    package_dir={'': 'src'},
    install_requires=['matplotlib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)