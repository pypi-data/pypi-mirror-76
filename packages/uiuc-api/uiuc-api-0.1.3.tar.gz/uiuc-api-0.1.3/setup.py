import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uiuc-api",
    version="0.1.3",
    author="Timothy Zhou",
    description="A python wrapper for UIUC's official REST API for querying course data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/TimothyZhou/uiuc_api",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests', 'lxml', 'pyyaml', 'lark-parser'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        "": ["*.lark"],
    }
)
