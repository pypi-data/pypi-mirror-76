import setuptools
from setuptools import find_packages
from setuptools import setup
import io
import re
import subprocess
import sys
import os
import getpass

    
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='robomax',
    version="8.0.4",
    description='Python code for versatile Functional Ontology Assignments for Metagenomes via Hidden Markov Model (HMM) searching with environmental focus of shotgun metaomics data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Alexander Brown, Richard White III',
    author_email='raw937@gmail.com',
    url='https://github.com/raw937/robomax',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=["Robomax_Wrapper_v8"],
    include_package_data=True,
    package_data={"": ["*.py", "LICENSE.txt"]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://github.com/raw937/robomax',
    },
    keywords=[
        'robomax', 'hmmer', 'Hidden Markov Model', 'hmm',
    ],
    python_requires='>=3.6.9',
)

path = "/home/%s/Desktop/robomax"% getpass.getuser()
path2 = "/home/%s/Desktop/robomax/osf_Files"% getpass.getuser()
access_rights = 0o755

##Creates the robomax folder

def robomax_dir():
    try:
        os.mkdir(path, access_rights)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s" % path),
        osf_Files_dir()

if __name__ == "__robomax_dir__":
    robomax_dir()

##Creates osf file directory and initiates OSF file download cmd create_osf_Files()

def osf_Files_dir():
    try:
        os.mkdir(path2, access_rights)
    except OSError:
        print ("Creation of the directory %s failed" % path2)
    else:
        print("Successfully created the directory %s" % path2),
        os.chdir(path2)
        create_osf_Files()

if __name__ == "__osf_Files_dir__":
    osf_Files_dir()

##Downloads OSF files to osf_File directory

def create_osf_Files():
    
    osf_cmd = "wget https://osf.io/72p6g/download -v -O FOAM_readme.txt"
    subprocess.call(['bash', '-c', osf_cmd])
    osf_cmd = "wget https://osf.io/muan4/download -v -O FOAM-onto_rel1.tsv"
    subprocess.call(['bash', '-c', osf_cmd])
    osf_cmd = "wget https://osf.io/2hp7t/download -v -O KO_classification.txt"
    subprocess.call(['bash', '-c', osf_cmd])
    osf_cmd = "wget https://osf.io/bdpv5/download -v -O FOAM-hmm_rel1a.hmm.gz"
    subprocess.call(['bash', '-c', osf_cmd])
        
if __name__ == "__create_osf_Files__":
    create_osf_Files()

robomax_dir()
