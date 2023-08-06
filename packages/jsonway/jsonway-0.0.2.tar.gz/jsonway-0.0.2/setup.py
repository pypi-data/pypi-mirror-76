import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsonway",
    version="0.0.2",
    author="Vishwanath",
    author_email="justvishu91@gmail.com",
    description="complete tool for the JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/umeshdhakar/sample-python-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
