from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="RubiksBlindfolded",
    version="1.0.4",
    description="A Python package of solving Rubik's Cube in Blindfolded technique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mn-banjar/RubiksBlindfolded",
    author="Moneera Banjar",
    author_email="mn.banjar@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["RubiksBlindfolded"],
    include_package_data=True,
    
)