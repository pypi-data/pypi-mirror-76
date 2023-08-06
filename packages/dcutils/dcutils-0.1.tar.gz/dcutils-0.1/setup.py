import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dcutils",
    version="0.1",
    author="Kiana Alessandra V. Villaera",
    author_email="kiana.villaera@senti.com.ph",
    description="A simple package for data center utilities",
    long_description="Contains everything you might need to perform essential data center functions",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/senti-techlabs/research/projects/senti-transfer-learning/-/tree/kiana-branch/data-pipeline/cloud_functions/data_center_utils",
    packages=['dcutils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)