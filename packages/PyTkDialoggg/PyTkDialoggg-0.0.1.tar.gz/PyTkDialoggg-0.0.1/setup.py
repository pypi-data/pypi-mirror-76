import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
print(setuptools.find_packages())
setuptools.setup(
    name="PyTkDialoggg", # Replace with your own username
    version="0.0.1",
    author="Arman Ahmadi",
    author_email="armanagha6@gmail.com",
    description="Module for Dialog",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lawbreakerr/Dialog",
    packages=['src'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
