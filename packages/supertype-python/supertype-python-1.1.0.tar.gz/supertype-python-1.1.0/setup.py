import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="supertype-python",
    version="1.1.0",
    author="Martin Letzgus",
    author_email="martin.letzgus@laposte.net",
    description="A simple recursive function that allows to give more information about an object than 'type' binded function",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MartinLetzgus/supertype",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)