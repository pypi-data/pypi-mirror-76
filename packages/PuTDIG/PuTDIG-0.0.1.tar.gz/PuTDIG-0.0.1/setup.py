# coding: utf-8
# pylint: skip-file
import os
import setuptools

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "An application to discover, generate and inject telemetry into RS3 modules."


requirements = [
    'pumpkin-supmcu',
    'putdig-common',
    'flask',
    'flask-wtf',
    'waitress'
]

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
elif os.environ.get('CI_JOB_ID'):
    version = os.environ['CI_JOB_ID']
else:
    version = '0.0.1'  # Makes sure the read the docs version can build.

setuptools.setup(
    name="PuTDIG",
    version=version,
    author="James Womack, Jack Hughes",
    author_email="info@pumpkininc.com",
    description="Web-based version of the PuTDIG suite of applications to discover, inject and generate telemetry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PumpkinSpace/PuTDIG",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['putdig=putdig_server.server:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.7',
    zip_safe=False,
    include_package_data=True
)
