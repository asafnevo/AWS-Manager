# AWS Manager
An open source project for managing your AWS VPC resources easily in your day to day coding.

This project was originally created to save our developers time when they need to update their code on our AWS IT infrastructure 
In addition, it gave us the ability to create an interface for executing common functions without teaching all our team how AWS works,
provide them login username and passwords, etc...

# Installation
   ```link to installation``` 
  
  After installing just run ```awsmanager```
   
# Functionality
  The project has the current abilities:

  Login to any type of instance in your infrastructure. If you have NAT instances you can use them to connect to your private instances
  Send git pull requests to your repository on the instance - specifying the branch you wish to pull

# AWS infrastructure
  The current version is built according to our VPC infrastructure require the right tagging in order to work properly.
  Feel free to update the code with your needs, or create a more generic version. 
  Just don't forget to update this repository with your changes :)

  Our infrastructure consists on this conventions:
  * We have a different VPC for development and production.
  * Each VPC contains different applications. 
  * Each of these applications have number of dedicated subnets for public instances according to the number of AWS Availability Zones in the current Region.
  * Each of these applications have number of dedicated subnets for private instances according to the number of AWS Availability Zones in the current Region.
  * Every application will have a NAT instance in one of his public subnets to allow access to the private subnets.

# Requirements
  **Credentials:**
  As part of the initial settings on first running the script, you will be asked to provide the path for the credential file for your AWS account.
  This can be  generated in the AWS Console under IAM service.
  The credentials must have a policy attached to them, which allows EC2 listing and connecting

  **Tagging:**
  This project filter and present the instances according to tagging conventions we use:

  *Mandatory tags:*
  * **Environment:** The name of the environment the instance belongs to (development, production, testings, etc) 
  * **Application:** The name of the application the instance is part of (API, Website, etc...)

*Optional Tags:*
  * **Remote Repository:** The remote git repository URL (without username or password) of the code installed on server. Without this tag, the pull function wont' be presented as an option
  * **Local Repository:** The local path for the git repository to update on pull requests. Without this tag, the pull function won't be presented as an option
  * **Public Domain:** if your instance has a public domain associated with (instance.your-domain.com), it will be shown as part of the information on the instance.


Would love to have your feedbacks, issues, etc...

## Please don't hesitate to contact us:
[Asaf Nevo](mailto:asaf.nevo@pico.buzz)

[Aviv Paz](mailto:aviv.paz@pico.buzz)

# Enjoy
