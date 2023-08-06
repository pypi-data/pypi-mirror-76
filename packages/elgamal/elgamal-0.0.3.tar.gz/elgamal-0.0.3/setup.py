import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elgamal", # Replace with your own username
    version="0.0.3",
    author="Sidq",
    author_email="dimax258223@gmail.com",
    description="Elgamal cryptography algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://t.me/sidqdev",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)