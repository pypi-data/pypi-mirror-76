import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="argilaparser", # Replace with your own username
    version="2.0.0",
    author="d4sein",
    author_email="williann.nasc@gmail.com",
    description="A lightweight object oriented lib for Python 3.8+ to help create CLI programs more easily. It has an elegant design taking advantage of built-in modules, and delivering a conducive environment to fast development and readability.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d4sein/Argila-Parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
