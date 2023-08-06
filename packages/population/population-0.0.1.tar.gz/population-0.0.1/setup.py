from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="population",
    version="0.0.1",
    description="A Python package to get population of countries.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/satyatomar/population.git",
    author="satyapal singh tomar",
    author_email="er.satyatomar@gmail.com",
    py_modules=["population"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    license="MIT",
    package_dir={'': 'population'},
)
