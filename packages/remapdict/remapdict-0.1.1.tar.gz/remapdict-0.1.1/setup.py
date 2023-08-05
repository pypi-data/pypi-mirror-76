import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="remapdict", # Replace with your own username
    version="0.1.1",
    author="Dylan Culfogienis",
    author_email="dculfogienis@expr.net",
    description="A convenience function for arbitrarily remapping dictionary keys, taking subsets, etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DylanCulfogienis/remapdict.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
