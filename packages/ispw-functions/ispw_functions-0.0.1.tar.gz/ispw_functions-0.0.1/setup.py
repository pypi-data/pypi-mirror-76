import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ispw_functions",
    version="0.0.1",
    author="Balthasar Hofer",
    author_email="lebalz@outlook.com",
    description="Helper functions for programming basics seminar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lebalz/ispw_functions",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)