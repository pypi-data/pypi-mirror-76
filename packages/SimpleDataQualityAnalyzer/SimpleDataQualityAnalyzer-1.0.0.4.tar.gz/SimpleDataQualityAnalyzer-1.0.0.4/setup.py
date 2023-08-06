from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="SimpleDataQualityAnalyzer",
    version="1.0.0.4",
    author="Stefan Kaspar",
    author_email="me@fullbox.ch",
    description="A python package that analyzes CSV files and generates a symple HTML report with some summary statistics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/debugair/simpledataqualityanalyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_data={
        "": [
                "Services/Templates/*.html",
                "Services/Templates/*.js"
            ],
    },
)
