import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="substack",
    version="0.0.1",
    author="Raghav Arora",
    author_email="agu94.raghav@gmail.com",
    description="A substack plugin for your website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raghavaro/substack-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
