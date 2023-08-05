# https://packaging.python.org/tutorials/packaging-projects/
import setuptools


setuptools.setup(
    name="GuessGames", 
    version="0.0.1",
    author="Jennifer Mason",
    author_email="jennifer.r.mason@btinternet.com",
    description="A higher or lower guessing game",
    #url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)