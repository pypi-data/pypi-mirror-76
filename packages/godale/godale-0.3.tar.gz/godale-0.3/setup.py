import os
from setuptools import setup, find_packages

with open("godale/__init__.py") as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

# use README for project long_description
with open("README.md") as f:
    readme = f.read()


def parse_requirements(file):
    return sorted(set(
        line.partition("#")[0].strip()
        for line in open(os.path.join(os.path.dirname(__file__), file))
    ) - set(""))


setup(
    name="godale",
    version=version,
    description="concurrent execution in various flavors",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Joachim Ungar",
    author_email="joachim.ungar@eox.at",
    license="MIT",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    setup_requires=["pytest-runner"],
    tests_require=parse_requirements("requirements_test.txt")
)
