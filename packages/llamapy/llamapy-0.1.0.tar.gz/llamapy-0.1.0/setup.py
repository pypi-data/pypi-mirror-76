import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="llamapy", 
    version="0.1.0",
    author="Alex Shannon",
    author_email="alex.shannon@airbnb.com",
    description="A package to make interfacing between Airpy and Google Sheets easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.musta.ch/alex-shannon/llamapy",
    download_url = 'https://git.musta.ch/alex-shannon/llamapy/llamapy-0.1.0.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)