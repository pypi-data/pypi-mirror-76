import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asyncjsonrpc",
    version="1.0.0",
    author="Hunter Smith",
    author_email="hunter@isrv.pw",
    description="Protocol-agnostic asynchronous Python JSON-RPC module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hunteradasmith/asyncjsonrpc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['aiohttp'],
)