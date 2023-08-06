import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="dustydata",
    version="0.0.2",
    author="Dustin Stringer",
    description="For my basic data cleaning and modeling needs",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/dustin-py/dustydata/tree/master/dustydata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6')
