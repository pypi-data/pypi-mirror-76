from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.read().splitlines()

setup(
    name="finutils",  # Replace with your own username
    version="0.0.2",
    license="MIT",
    author="Hemanth Bollamreddi",
    author_email="blmhemu@gmail.com",
    description="Finutils is a collection of some finance related python utilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blmhemu/finutils",
    keywords="finutils, cached pandas datareader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=install_requires,
    python_requires=">=3.7",
    platforms=["any"],
)
