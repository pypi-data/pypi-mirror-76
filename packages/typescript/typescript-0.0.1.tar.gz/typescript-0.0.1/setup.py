import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typescript", # Replace with your own username
    version="0.0.1",
    author="Microsoft Corporation",
    author_email="ian.sawyer@microsoft.com",
    description="TypeScript for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ian-sawyer/TypeScript-for-Python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
