from setuptools import setup, find_packages
import sys, os

version = '0.1'
description = "Manage your AWS resources easily"

setup(
      name="AWS Manager",
      description=description,
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      entry_points={
        'console_scripts': [
            'awsmanager = aws_manager.main:main',
            ],
        },
      zip_safe=False,
      include_package_data=True
      )
