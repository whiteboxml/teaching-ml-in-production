# ML-IN-PRODUCTION-MADRID

This repository contains all materials from the workshop about __putting Machine Learning models to production__ we 
teached in September 2019 at [IronHack](http://www.ironhack.com/en).

## Approach

This is a practical workshop with the goals of learning the following concepts:

* How to setup MLFLow, a tool for ML experiment tracking and model deploying, from zero to hero.
* How to track ML experiments with MLFLow
* How to put models to production with MLFLow.
* How to deploy models to production in AWS Sagemaker with just a couple lines of code.
* How to setup Apache Airflow, a powerful tool to design, schedule and monitor workflows.
* How to create workflows that take advantage of deployed models.

In order to follow tutorials in a standard setup, there is a Linux VM included in this repository 
with repository itself and conda preinstalled. Please download VirtualBox and import `vm/ubuntu.ova`.

VM login credentials are:

- username: ubuntu
- password: ubuntu

In case you want to follow examples in this repo using your very own setup, we highly recommend using an
[Ubuntu 18.04](http://releases.ubuntu.com/18.04/ubuntu-18.04.3-live-server-amd64.iso) 
machine with [conda](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh) installed.

### Calendar

- Friday 27/09/2019 from 17 to 20h
    * Introduction to Machine Learning in Production
    * Introduction to MLFlow, MLFLow full setup
    * Introduction to Dataset and Business Case (Renfe AVE ticket price forecasting)
    * MLFLow training API

- Saturday from 10 to 20h
    * MLFLow deployment API
    * Python Virtual Environments distribution
    * AWS model deployment with SageMaker
    * Introduction to Apache Airflow
    * Airflow orchestration

### Business Case

All examples will use our [dataset](https://www.kaggle.com/thegurusteam/spanish-high-speed-rail-system-ticket-pricing) 
about high speed train tickets in Spain. 
The following use cases are covered here:

Unsupervised learning - high speed train tickets clustering using the following algorithms:
- Dimensionality reduction with UMAP
- HDBSCAN clustering
- Model to production using MLFlow so that the REST API returns a cluster ID for new tickets

Supervised learning - high speed train tickets forecasting using the following algorithms:
- XGBoost implementation of AWS Sagemaker (both cloud training and model deployment)
- scikit-learn Random Forest (local training and cloud deployment in AWS Sagemaker)
  
Model deployment:
- Putting models to production in virtually any linux machine or server
- Putting model to production in cloud with AWS SageMaker

Scheduling:
- Orchestration of (batch) clustering and price forecasting for new data using Apache Airflow
