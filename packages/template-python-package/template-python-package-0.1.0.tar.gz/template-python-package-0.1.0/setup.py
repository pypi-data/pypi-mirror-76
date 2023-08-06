from setuptools import setup, find_packages
from pathlib import Path

requirements = []

__version__ = "0.1.0"


# Add README to PyPI
this_dir = Path(__file__).parent
with open(Path.joinpath(this_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="template-python-package",
    version=__version__,
    packages=find_packages(),
    license="MIT",
    author="Umesh Timalsina",
    author_email="umesh.timalsina@vanderbilt.edu",
    url="https://github.com/umesh-timalsina/template-python-package",
    install_requires=requirements,
    python_requires=">=3.6, <4",
    include_package_data=True,
    zip_safe=False,
    description="A template python package for testing pypi releases with azure pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
