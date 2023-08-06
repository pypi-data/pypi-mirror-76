import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leglib", # Replace with your own username
    version="0.0.3",
    author="Joe Legner",
    author_email="joelegner@gmail.com",
    description="My personal Python shared package with lots of weird stuff.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joelegner/leglib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
