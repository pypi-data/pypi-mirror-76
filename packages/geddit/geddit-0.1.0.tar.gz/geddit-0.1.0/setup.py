import os

from setuptools import setup, find_packages


def load_requirements():
    """
    Load requirements file and return non-empty, non-comment lines with leading and trailing
    whitespace stripped.

    """
    with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
        return [
            line.strip() for line in f
            if line.strip() != '' and not line.strip().startswith('#')
        ]


with open("README.md") as fobj:
    long_description = fobj.read()


setup(
    name="geddit",
    version="0.1.0",
    author="University of Cambridge Information Services",
    author_email="devops+geddit@uis.cam.ac.uk",
    description="Zero-configuration fetching of configuration resources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.developers.cam.ac.uk/uis/devops/lib/geddit/",
    packages=find_packages(),
    install_requires=load_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
