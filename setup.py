from setuptools import setup, find_packages
import os

version = '0.2'
description = "An open source project for managing your AWS resources easily in your day to day coding"
long_description = "README.md"
author = 'Asaf Nevo, Aviv Paz',
author_email = 'asafnevo1@gmail.com, avivpaz43556@gmail.com'
license_type = "GNU"
keywords = 'aws ec2 amazon servers vpc awscli'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
        author=author,
        author_email=author_email,
        name="AWS Manager",
        version=version,
        license=license_type,
        description=description,
        long_description=read(long_description),
        packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
        install_requires=["boto3"],
        entry_points={
            'console_scripts': [
                'awsmanager = aws_manager.main:main',
            ],
        },
        keywords=keywords,
        zip_safe=False,
        include_package_data=True
)
