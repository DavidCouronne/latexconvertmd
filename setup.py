import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="latexconvertmd",
    version="0.0.8",
    author="David Couronné",
    author_email="couronne.david@gmail.com",
    description="Convertion LaTeX en Markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DavidCouronne/latexconvertmd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)