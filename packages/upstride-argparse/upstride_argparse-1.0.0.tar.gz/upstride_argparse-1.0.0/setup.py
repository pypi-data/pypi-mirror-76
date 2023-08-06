import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="upstride_argparse",
    version="1.0.0",
    author="Upstride",
    author_email="pypi@upstride.io",
    description="Simple and efficient argument parser for every python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UpStride/betterargparse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite="nose.collector",
    tests_require=['nose'],
    install_requires=[
        'PyYAML',
    ],
)