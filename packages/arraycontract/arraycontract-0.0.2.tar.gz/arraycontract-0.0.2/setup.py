import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arraycontract",
    version="0.0.2",
    author="cjwcommuny",
    author_email="cjwcommuny@outlook.com",
    description="Check shape, ndim and dtype of tensor/ndarray of input of function",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cjwcommuny/array_contract",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
