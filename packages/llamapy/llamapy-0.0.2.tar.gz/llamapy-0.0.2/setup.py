import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="llamapy", 
    version="0.0.2",
    author="Alex Shannon",
    author_email="alex.shannon@airbnb.com",
    description="A package to make interfacing between Airpy and Google Sheets easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.musta.ch/alex-shannon/llamapy",
    packages=setuptools.find_packages(),
    install_requires=['gspread'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)