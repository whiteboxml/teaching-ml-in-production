# ml-in-production-madrid

## Approach

- UMAP over one destination + HDBSCAN served by MLFlow so that the REST API answers with the cluster ID
- Orchestration of new data with Airflow
- Put this model into production with SageMaker
- Upload csv to test AML
