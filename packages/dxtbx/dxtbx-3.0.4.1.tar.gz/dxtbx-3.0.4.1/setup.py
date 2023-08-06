import sys
from setuptools import setup, find_packages

requirements = ["dials-data", "procrunner"]
test_requirements = ["mock", "pytest"]

setup(
    author="DIALS collaboration",
    author_email="scientificsoftware@diamond.ac.uk",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    description="Diffraction Experiment Toolbox",
    install_requires=requirements,
    license="BSD license",
    include_package_data=True,
    keywords="dials",
    name="dxtbx",
    packages=find_packages(),
    package_dir={"dxtbx": "../dxtbx"},
    data_files=[
        ("dxtbx", ["LICENSE.txt", "__init__.py", "libtbx_refresh.py", "conftest.py"])
    ],
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/cctbx/dxtbx",
    version="3.0.4.1",
    zip_safe=False,
)
