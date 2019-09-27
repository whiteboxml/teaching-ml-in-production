# Deployment of Machine Learning models on AWS

## Introduction

AWS is one of the most popular PaaS services available on the market. It powers a high % of the internet and offers a 
wide range of services interesting to train and deploy Machine Learning models. Its most famous is 
[SageMaker](https://aws.amazon.com/sagemaker/), an integrated solution for training and deploy models. Another 
interesting option is using spot instances to train complex models on expensive hardware for a fraction of the price.
This function is also integrated in SageMaker now.

## Getting ready for AWS

### Create an account

First thing needed is creating an account. It requires a credit card and takes time to be active. Please check 
[this](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) link to learn about
how to create an AWS account. It takes a couple of days to have it fully working.

### Core components of AWS

There are some core components of AWS, being many other services just wrappers around those components. The most
important are:

* EC2: computing
* S3: storage

### Getting credentials to use AWS programmatically

First thing needed for using AWS from Python scripts is getting AWS credentials. To enable a programmatic access, the
service known as IAM: Identity and Access Management service. Please be aware of the region you are working on: for
this workshop, the region `eu-west-1`, located in Ireland, will be used. To access IAM, follw
[this](https://console.aws.amazon.com/iam/home?region=eu-west-1#/home) link.

Once in AWS: 

* Create a new user with admin permissions
* Check programmatic access checkbox
* Attach directly administrative policies to the user
* Copy `Access key ID` and `Secret access key` to a safe place

### Creating credentials and config files

Using credentials, a couple of files must be created inside a folder called `.aws` in user `home` folder:

* credentials (text file with no extension):

```ini
[default]
aws_access_key_id=<your_access_key>
aws_secret_access_key=<your_secred_key>
```

* config (text file with no extension):

```ini
[default]
region=eu-west-1
output=json
```

### Create a SageMaker execution role

From IAM console, create an execution role with full AWS SageMaker execution access.

### Installing aws cli

Next, install AWS cli interface:

* `sudo apt install awscli`

### Install boto3 and sagemaker api in your virtual environment

Those libraries can lead to errors while installing, please be careful and create a new virtual environment. A
requests file to run `aws_deployment.ipynb` notebook is provided in config folder. First create a new environment called
`aws_env`:

* `conda create -n aws_env`
* `conda activate aws_env`
* `conda install python`
* `pip install -r /path/to/requests.txt`
