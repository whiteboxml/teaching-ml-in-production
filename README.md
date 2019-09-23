# ml-in-production-madrid

## Approach

### Calendar

- Friday 27/09/2019
    * Introduction
    * Dataset and business case
    * MLFlow, full production setup
    * MLFLow, training a model

- Saturday
    * MLFLow, serving a model
    * Apache Airflow, orchestrating processes
    * AWS, core components. Training models the cheap way
    * AWS, SageMaker. From modeling to production

### Business Case

Unsupervised learning:
    - UMAP over one origin - destination pair (for example Madrid - Barcelona)
    - HDBSCAN clustering served by MLFlow so that the REST API answers with the cluster ID for new trips

Scheduling:
    - Orchestration of new data with Apache Airflow

Cloud solutions
    - Put this model into production with SageMaker
    - Amazon Machine Learning (for non-coders)
