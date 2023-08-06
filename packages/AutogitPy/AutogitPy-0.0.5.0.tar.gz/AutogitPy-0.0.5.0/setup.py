import setuptools

with open("README.md", "r") as fh:
    long_description=fh.read()
        

setuptools.setup(
    name="AutogitPy", # Replace with your own username
    version="0.0.5.0",
    author="Saran,Abhilash,Abhiraman,Tarun",
    author_email="unofficialcredentials@gmail.com",
    description="A package which automates the process of git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sites.google.com/view/docs-autogitpy/home",
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


