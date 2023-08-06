from setuptools import setup, Extension
from Cython.Build import cythonize 

import os 
os.environ["CC"] =  "clang++"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ms_map", 
    version="1.0.0", 
    url="https://github.com/zmcgrath96/ms_map", 
    author="Zachary McGrath", 
    author_email="zmcgrath96@gmail.com", 
    description="A datastructure for efficient storage of mass spectrometry data", 
    long_description=long_description, 
    long_description_content_type="text/markdown", 
    keywords="bioinformtatics mass_spectrometry ms map", 
    ext_modules=cythonize(Extension(
        "ms_map", 
        ["ms_map.pyx"], 
        language="c++", 
        extra_compile_args=["-std=c++11"]
    ))
)