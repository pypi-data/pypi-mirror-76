import setuptools


with open("README.md", "r") as fh:
	long_description = fh.read()


setuptools.setup(
	name="LazyIter-teshnizi",
	version="0.2",
	author="Ali AhmadiTeshnizi",
	author_email="aliahmaditeshnizi@gmail.com",
	description="LazyIter ICML2020",
	long_description="Package for the ICML paper  \"LazyIter: A Fast Algorithm for Counting Markov Equivalent DAGs and Designing Experiments\"",
	long_description_content_type="text/markdown",
    url="https://github.com/teshnizi/LazyIter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
