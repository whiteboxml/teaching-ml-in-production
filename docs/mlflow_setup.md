# MLFlow Setup - Tracking Server

This guide will show you how to setup a production MLFlow Tracking Server, so
that you can keep track of your experiments and enjoy a full user
experience with MLFlow.

The first thing we need to configure is the environment.

## Environment

Let's create a new Conda environment as it will be the place where MLFlow
will be installed:

```bash
conda create -n mlflow_env
conda activate mlflow_env
```

Then we have to install the MLFlow library:

```bash
conda install python
pip install mlflow
```

Run the following command to check that the installation was successful:

```bash
mlflow --help
```

We'd like our Traking Server to have a Postgres database as a backend for
storing metadata, so the first step will be installing PostgreSQL:

```bash
sudo apt-get install postgresql postgresql-contrib postgresql-server-dev-all
```

Check installation connecting to the database:

```bash
sudo -u postgres psql
```

After the installation is successful, let's create an user and a database
for the Traking Server:

```sql
CREATE DATABASE mlflow;
CREATE USER mlflow WITH ENCRYPTED PASSWORD 'mlflow';
GRANT ALL PRIVILEGES ON DATABASE mlflow TO mlflow;
```

As we'll need to interact with Postgres from Python, it is needed to install
the psycopg2 library. However, to ensure a successful installation we need 
to install the gcc linux package before:

```bash
sudo apt install gcc
pip install psycopg2
```

The last step will be creating a directory in our local machine for our 
Tracking Server to log there the Machine Learning models and other artifacts.
Remember that the Postgres database is only used for storing metadata
regarding those models (imaging adding a model or a virtual environment
to a database). This directory is called artifact URI:

 ```bash
mkdir ~/mlruns
```

## Run

Everything is now setup to run the Tracking Server. Then write the following
command:

```bash
mlflow server --backend-store-uri postgresql://mlflow:mlflow@localhost/mlflow --default-artifact-root file:/home/your_user/mlruns -h 0.0.0.0 -p 8000
```

Now the Tracking server should be available a the following URL: 
http://0.0.0.0:8000. However, if you Ctrl-C or exit the terminal, the
server will go down.

## Production

If you want the Tracking server to be up and running after restarts and 
be resilient to failures, it is very useful to run it as a systemd service.

You need to go into the /etc/systemd/system folder and create a new file called
mlflow-tracking.service with the following content:
 
```
[Unit]
Description=MLFlow tracking server
After=network.target

[Service]
Restart=on-failure
RestartSec=30
StandardOutput=file:/path_to_your_logging_folder/stdout.log
StandardError=file:/path_to_your_logging_folder/stderr.log
ExecStart=/bin/bash -c 'PATH=/path_to_your_conda_installation/envs/mlflow_env/bin/:$PATH exec mlflow server --backend-store-uri postgresql://mlflow:mlflow@localhost/mlflow --default-artifact-root file:/home/your_user/mlruns -h 0.0.0.0 -p 8000'

[Install]
WantedBy=multi-user.target
```

After that, you need to activate and enable the service with the following
commands:

```bash
sudo mkdir -p /path_to_your_logging_folder
sudo systemctl daemon-reload
sudo systemctl enable mlflow-tracking
sudo systemctl start mlflow-tracking
```

Check that everything worked as expected with the following command:

```bash
sudo systemctl status mlflow-tracking
```

You should see an output similar to this:

```
● mlflow-tracking.service - MLFlow tracking server
   Loaded: loaded (/etc/systemd/system/mlflow-tracking.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2019-09-27 09:02:11 UTC; 14s ago
 Main PID: 10357 (mlflow)
    Tasks: 10 (limit: 4915)
   CGroup: /system.slice/mlflow-tracking.service
           ├─10357 /path_to_your_conda_installation/envs/mlflow_env/bin/python /home/ubuntu/miniconda3/envs/mlflow_env/bin/mlflow s
           ├─10377 /path_to_your_conda_installation/envs/mlflow_env/bin/python /home/ubuntu/miniconda3/envs/mlflow_env/bin/gunicorn
           ├─10381 /path_to_your_conda_installation/envs/mlflow_env/bin/python /home/ubuntu/miniconda3/envs/mlflow_env/bin/gunicorn
           ├─10383 /path_to_your_conda_installation/envs/mlflow_env/bin/python /home/ubuntu/miniconda3/envs/mlflow_env/bin/gunicorn
           ├─10385 /path_to_your_conda_installation/envs/mlflow_env/bin/python /home/ubuntu/miniconda3/envs/mlflow_env/bin/gunicorn
           └─10386 /path_to_your_conda_installation/envs/mlflow_env/bin/python /home/ubuntu/miniconda3/envs/mlflow_env/bin/gunicorn

Sep 27 09:02:11 ubuntu systemd[1]: Started MLFlow tracking server.
```
 
 You can now restart your machine and the MLFlow Tracking Server will be
 up and running after this restart.
 