import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parsexml", # Replace with your own username
    version="0.0.1",
    author="John Burt",
    author_email="",
    description="Simple XML parsing to python structure.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alphabet5/parsexml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={"parsexml.parsexml": [".rst = parsexml:parsexml"]},
)
