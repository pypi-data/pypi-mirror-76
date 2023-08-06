from setuptools import setup

import setuptools

#with open("README.md", "r") as fh:
#   long_description = fh.read()

setuptools.setup(
    name="pandas-stocks-tech-analysis", # Replace with your own username
    version="0.0.2",
    author="'Uday Gupta & Rahul Dayma'",
    author_email="udaygupta9594@gmail.com,rahuldayma07.rd@gmail.com",
    description="We used the Bombay stock exchange (BSE) Data to calculate different technical indicators for the batter stock analysis in using pandas",
 #   long_description=long_description,
    url="https://github.com/uday171197/pandas-stocks-tech-analysis,https://github.com/rahuldayma7/pandas-stocks-tech-analysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
