from setuptools import setup

# This call to setup() does all the work

with open("README.md","r") as fh:
    long_description=fh.read()
setup(
    name="preprocessutils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.0.1",
    author="Punit Nanda",
    author_email="punit.nanda01@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    py_modules=["preprocessutils"],
    package_dir={'':'src'},
    install_requires=["imbalanced-learn", "numpy", "pandas"],
)