import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dltkai",
    version="1.0.9",
    author="DLTK",
    author_email="connect@qubitai.tech",
    description="Python Client for DLTK.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dltk-ai/dltkai-sdk",
    packages=setuptools.find_packages(),
    install_requires=[
        'Keras==2.3.1',
        'tensorflow==2.2.0rc2',
        'imageai==2.1.5'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)