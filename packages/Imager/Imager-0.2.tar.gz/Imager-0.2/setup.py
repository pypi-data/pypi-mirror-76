try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "Imager",
    version = "0.2",
    packages=['Imager'],
    description = "A Image Finder Search Engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = "Muhammad Hanan Asghar",
    author_email = "muhammadhananasghar@gamil.com",
    url="https://github.com/MuhammadHananAsghar",
    install_requires = [
        "bs4",
        "requests",
        "wheel",
        "fake-useragent"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
