import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hiarjun", # Replace with your own username
    version="0.0.1",
    author="Arjun Dandagi",
    author_email="dandagi.arjun95@gmail.com",
    description="A package that prints Hi n times",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arjundandagi/hiarjun",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
