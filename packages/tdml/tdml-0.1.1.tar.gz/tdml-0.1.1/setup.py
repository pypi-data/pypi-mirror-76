import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tdml",
    version="0.1.1",
    author="Zecheng Zhang",
    author_email="zecheng@cs.stanford.edu",
    description="Transform Dataframe for Machine Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zechengz/tdml",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
