import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="portfolio-report-Ross-McCandless",
    version="0.0.1",
    author="Ross McCandless",
    author_email="rmccandless1100@conestogac.on.ca",
    description="Stock portfolio report program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sheridan-python/assignment-7-Ross-McCandless",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
