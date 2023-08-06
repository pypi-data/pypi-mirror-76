import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mmtapi", # Replace with your own username
    version="0.0.2",
    author="Samuel Wyatt",
    author_email="swyatt@email.arizona.edu",
    description="An API wrapper for uploading Targets to the MMT observation queue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swyatt7/mmtapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
