import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rsaes", # Replace with your own username
    version="0.0.1",
    author="Sidq",
    author_email="dimax258223@gmail.com",
    description="RSA + AES cryptography algorithms",
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