import pkg_resources
import setuptools

pkg_resources.require(['pip >= 19.3.1'])


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="amlutils",
    version="1.8",
    author="Parv Oberoi",
    author_email="amlutils@gmail.com",
    description="A collection of useful methods and utilities for Machine Learning Projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/parvoberoi/amlutils",
    license='Apache Software License',
    packages=setuptools.find_packages(),
    # TODO: where condition option leads to module not found error
    # packages=setuptools.find_packages(where="amlutils"),
    # package_dir={
    #     "": "amlutils",
    # },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.18.3",
        "opencv-python>=4.2.0.34",
        "requests>=2.23.0",
    ]
)
