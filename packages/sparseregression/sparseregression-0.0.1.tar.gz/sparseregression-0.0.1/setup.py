import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sparseregression",
    version="0.0.1",
    author="Eugenio Zuccarelli",
    author_email="ezucca@mit.edu",
    description="Sparse Regression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ezuccarelli/sparseregression",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)