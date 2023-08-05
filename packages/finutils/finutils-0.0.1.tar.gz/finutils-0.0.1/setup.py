from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="finutils",  # Replace with your own username
    version="0.0.1",
    license="MIT",
    author="Hemanth Bollamreddi",
    author_email="blmhemu@gmail.com",
    description="Finutils is a collection of some finance related python utilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blmhemu/finutils",
    keywords="pandas, cached, pandas datareader, cache reader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas>=1.1.0", "pandas_datareader>=0.9.0"],
    python_requires=">=3.7",
    platforms=['any'],
)
