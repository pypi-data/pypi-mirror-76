from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="chopchop",
    version="1.0.0",
    description="Make logs digestible",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.github.com/seongminp/chopchop",
    keywords="Log management",
    author="Seongmin Park",
    author_email="llov0708@gmail.com",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",
)
