import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="decev",
    version="0.0.1",
    author="Dan W-B",
    author_email="d@nielwb.com",
    description="Event handlers with decorators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dantechguy/decev",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
