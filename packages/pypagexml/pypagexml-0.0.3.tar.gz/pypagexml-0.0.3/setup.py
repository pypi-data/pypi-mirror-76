from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pypagexml',
    version='0.0.3',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    author="Alexander Gehrke",
    author_email="gehrke@informatik.uni-wuerzburg.de",
    url="https://gitlab2.informatik.uni-wuerzburg.de/alg81dm/pypagexml.git",
    install_requires=open("requirements.txt").read().split(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
    ],
    keywords=['pagexml', 'page segmentation', 'layout'],
    data_files=[('', ["requirements.txt"])],
)
