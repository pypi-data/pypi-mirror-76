import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="DetectBinod",

    version="0.0.2",

    author="Akshay Pawar",
 
    
    author_email="akshupatil665@gmail.com",
 
   
    description="Detect Binod In Files",
 
    long_description=long_description,
    
    long_description_content_type="text/markdown",

    install_requires=[
      "PyPDF2",
      "xlrd",
      "python-docx",
      "python-pptx",
   ],
    license="MIT",

    packages=setuptools.find_packages(),
 
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)