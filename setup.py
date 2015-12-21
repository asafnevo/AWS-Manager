from setuptools import setup, find_packages
import sys, os

version = '0.2'
description = "An open source project for managing your AWS resources easily in your day to day coding"

setup(
      name="AWS Manager",
      version=version,
      description=description,
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
