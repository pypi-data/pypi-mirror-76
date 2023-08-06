import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Portfolio Report Generator", # Replace with your own username
    version="0.0.1",
    author="Chandan Pai",
    author_email="chandanrpai@gmail.com",
    description="Generate report for a given stock portfolio.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chandanrpai/assignment-7-chandanrpai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
