import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dustydata",
    version="0.0.4",
    author="Dustin Stringer",
    author_email="dustinstri92@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dustin-py/Packages/tree/master/dustydata",
    packages=setuptools.find_packages(),
    python_requires='>=3.6'
)
