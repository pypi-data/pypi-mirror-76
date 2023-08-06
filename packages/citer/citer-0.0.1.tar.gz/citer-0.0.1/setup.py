import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()
long_description = ""

setuptools.setup(
    name="citer", # Replace with your own username
    version="0.0.1",
    author="Yuanchao Zhang",
    author_email="logstarx@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
