import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hopy",
    version="0.0.2",
    author="Arpit Singla",
    author_email="arpitsingla96@gmail.com",
    description="A high level language for predicate evaluation on JSON using JsonPath expressions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arpitsingla96/hopy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    extras_require={
        "jsonpath_ng": ["jsonpath-ng>=1.5.0"]
    }
)
