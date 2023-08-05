from setuptools import setup

from dnxsso import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="dnxsso",
    version=__version__,
    description="Sync up AWS CLI v2 SSO login session to legacy CLI v1 credentials",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DNXLabs/dnxsso",
    author="DNX Solutions",
    author_email="contact@dnx.solutions",
    license="MIT",
    packages=["dnxsso"],
    zip_safe=False,
    entry_points={
        "console_scripts": ["dnxsso=dnxsso.cli:main"],
    },
    extras_require={
        "test": [
            "pytest",
            "pytest-cov",
            "flake8",
            "mockito",
            "cli-test-helpers",
            "nose2",
            "coveralls",
        ],
        "dev": [
            "twine",
            "setuptools",
            "wheel",
        ],
    }
)
