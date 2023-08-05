import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eve-simple-esi", # Replace with your own username
    version="0.0.2",
    author="Zorg Programming",
    author_email="dr.danio@gmail.com",
    description="The Python 3+ library for simple and fast work with https://esi.evetech.net data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drdanio/eve-simple-esi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)