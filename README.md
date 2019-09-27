# ml-in-production-madrid

This repository contains all materials from the workshop 
**Machine Learning in Production: Madrid**:

## Approach

This is a practical workshop. There is a Linux VM included in this repository. With repository itself and conda
preinstalled. Please download VirtualBox and import `vm/ubuntu.ova`. Credentials are:

    - username: ubuntu
    - password: ubuntu

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

Unsupervised learning:
    - UMAP over one origin - destination pair (for example Madrid - Barcelona)
    - HDBSCAN clustering served by MLFlow so that the REST API answers with the cluster ID for new trips
    
Supervised learning:
    - Price forecasting for new tickets

Scheduling:
    - Orchestration of new data with Apache Airflow

Cloud solutions
    - Put this model into production with SageMaker
    - Amazon Machine Learning (for non-coders)