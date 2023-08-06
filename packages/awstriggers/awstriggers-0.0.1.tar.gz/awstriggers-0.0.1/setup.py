import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awstriggers",
    version="0.0.1",
    author="JevyanJ",
    author_email="jjrg184@gmail.com",
    description="Simple classes for AWS trigger records and events.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JevyanJ/awstriggers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
