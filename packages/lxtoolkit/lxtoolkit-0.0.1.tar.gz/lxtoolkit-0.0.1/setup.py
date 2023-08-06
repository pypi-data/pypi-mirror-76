from setuptools import setup, find_packages

setup(
    name = "lxtoolkit",
    version = "0.0.1",
    keywords = ("pip", "pytorch", "tutorial"),
    description = "a simple toolkit based on torch and torchvision",
    long_description = "a simple toolkit based on torch and torchvision",
    license = "MIT",

    url = "",         
    author = "blackbeanman123",                         
    author_email = "blackbeanman123@gmail.com",    

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)