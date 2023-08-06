from lists import __VERSION__
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="list-manager",
    version=__VERSION__,
    author="Raghav Nair",
    author_email="nairraghav@hotmail.com",
    description="A simple CLI tool that allows management of lists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nairraghav/lists-library",  #
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['list_manager=lists:main'],
    }
)
