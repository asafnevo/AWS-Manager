from setuptools import setup, find_packages
import os

version = '0.2'
description = "An open source project for managing your AWS resources easily in your day to day coding"
long_description = "README.md"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
        name="AWS Manager",
        version=version,
        description=description,
        long_description=read(long_description),
        packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
        install_requires=["boto3"],
        entry_points={
            'console_scripts': [
                'awsmanager = aws_manager.main:main',
            ],
        },
        zip_safe=False,
        include_package_data=True
)
