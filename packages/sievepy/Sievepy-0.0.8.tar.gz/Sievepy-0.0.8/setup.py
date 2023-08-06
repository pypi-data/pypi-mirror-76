import setuptools

with open("README.md", "r") as fh:
    long_description=fh.read()
        

setuptools.setup(
    name="Sievepy",
    version="0.0.8",
    author="Abhilash",
    author_email="abhilash11addanki@gmail.com",
    description="A package which efficiently finds the prime numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abhilash11Addanki/Sievepy",
    packages=setuptools.find_packages(),
    keywords="configuration core yaml ini json environment",
    license="MIT",
    
    classifiers=[
        
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
