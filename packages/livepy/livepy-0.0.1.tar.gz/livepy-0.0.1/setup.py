import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="livepy", # Replace with your own username
    version="0.0.1",
    author="Prashant Rawat",
    author_email="prashant.rawat216@gmail.com",
    description="A live python shell to run code online.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prshnt19/LivePy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
