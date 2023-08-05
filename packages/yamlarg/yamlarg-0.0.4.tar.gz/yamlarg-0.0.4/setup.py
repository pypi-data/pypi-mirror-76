import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yamlarg", # Replace with your own username
    version="0.0.4",
    author="John Burt",
    author_email="",
    description="Easy YAML arguments for python scripts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alphabet5/yamlarg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={"yamlarg.parse": [".rst = yamlarg:parse"]},
)