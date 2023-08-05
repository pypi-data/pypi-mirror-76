import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pryzm",
    version="0.1.2",
    author="Efrain Olivares",
    author_email="efrain.olivares@gmail.com",
    description="Basic support for asci color text on linux terminals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hydraseq/pryzm",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
