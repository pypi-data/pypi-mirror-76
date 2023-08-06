import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plotarchive", # Replace with your own username
    version="0.0.3",
    author="Chris Buswinka",
    author_email="buswinka@gmail.com",
    description="An easy method to save code and data that generates scientific plots.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/buswinka/plotarchive",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)