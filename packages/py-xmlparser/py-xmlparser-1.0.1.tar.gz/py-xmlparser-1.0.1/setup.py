import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-xmlparser",
    version="1.0.1",
    author="Shachar Oren",
    author_email="shr.or91@gmail.com",
    description="A python package for parsing xml files into data structures.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shachar-oren/xmlparser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)