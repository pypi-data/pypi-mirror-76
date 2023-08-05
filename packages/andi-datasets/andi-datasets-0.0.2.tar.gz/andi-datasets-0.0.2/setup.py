import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="andi-datasets", 
    version="0.0.2",
    author="Gorka Munoz-Gil",
    author_email="munoz.gil.gorka@gmail.com",
    description="The Anomalous Diffusion Challenge package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AnDiChallenge/ANDI_datasets",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
