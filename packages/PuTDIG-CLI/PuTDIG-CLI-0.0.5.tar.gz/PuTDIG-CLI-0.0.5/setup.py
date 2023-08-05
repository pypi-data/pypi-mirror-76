# coding: utf-8
# pylint: skip-file
import os
import setuptools

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A library to interface with Pumpkin SupMCU modules via I2C."

# try:
#     with open("requirements.txt", 'r') as f:
#         requirements = f.read()
#         requirements = requirements.splitlines()
#         requirements = [r for r in requirements if r.strip() != '']
# except FileNotFoundError:
#     # User installing from pip
#     requirements = [
#         'pumpkin-supmcu',
#         'pumpkin-supmcu-i2cdriver',
#         'pumpkin-supmcu-smbus',
#         'putdig-common'
#     ]
requirements = [
    'pumpkin-supmcu',
    'putdig-common'
]

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
elif os.environ.get('CI_JOB_ID'):
    version = os.environ['CI_JOB_ID']
else:
    version = '0.0.5'  # Makes sure the read the docs version can build.

setuptools.setup(
    name="PuTDIG-CLI",
    version=version,
    author="James Womack, Jack Hughes",
    author_email="info@pumpkininc.com",
    description="Common interface and business logic for PuTDIG and PuTDIG-CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PumpkinSpace/PuTDIG-CLI",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['puminj=putdig_cli.puminj:execute',
                            'pumgen=putdig_cli.pumgen:execute',
                            'pumqry=putdig_cli.pumqry:execute']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.7',
)
