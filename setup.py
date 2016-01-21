from setuptools import setup, find_packages
import os

name = "AWS-Manager"
version = '0.3c'
description = "An open source project for managing your AWS resources easily in your day to day coding"
long_description = "README.md"
author = 'Asaf Nevo, Aviv Paz',
author_email = 'asafnevo1@gmail.com, avivpaz43556@gmail.com'
license_type = "GNU"
keywords = 'aws ec2 amazon servers vpc awscli'


def read(file_name):
    """
    Read a text file in the Root directory
    :param str file_name: the name of the file
    :return: the content of the text file
    :rtype: str
    """
    return open(os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)).read()


setup(
        author=author,
        author_email=author_email,
        name=name,
        version=version,
        license=license_type,
        description=description,
        # long_description=read(long_description),
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
