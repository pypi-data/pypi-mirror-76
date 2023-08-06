import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydecibel", # Replace with your own username
    version="0.0.1",
    author="Johan Jatko",
    author_email="armedguy@ludd.ltu.se",
    description="Turn your infrastructure up to eleven!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArmedGuy/decibel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)