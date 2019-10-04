# Airflow setup guide

## Introduction

The goal of this session is to achieve full autonomy by installing and configuring Airflow with a standard and easy configuration 
(but effective for most projects), as well as learn the basic functionalities about workflows creation and getting familiar with 
Airflow web interface.

This introduction will explain the basics concepts of Airflow using a business case that will be developed during this session.

This case study is the creation of a pipeline that, using this dataset about High Speed train tickets, try to predict its price
and cluster the ticket belong (two models, one supervised and other unsupervised have been training before, and are available through
different endpoints).

1. Mocks user alarms for Renfe tickets. Those alarms are just a ticket scrapped in a very particular point of time we want to track.
2. Predicts future (next week price), and compare to original price.
3. Perform a clustering of ticket (just for learning purposes).

## Apache Airflow: motivation, advantages and disadvantages

### Current situation and motivation for Airflow existance

Currently the management and orchestration of processes has been carried out using various tools and methodologies, for example:

* Shell scripts.
* Python scripts.
* R scripts.
* Jupyter Notebooks.
* Cron
* Oozie

At the same time, the Data practice has evolved due to:

* More data accumulated by companies. They want to use that data.
* Companies whose activity was not oriented to the storage and exploitation of the data from the beginning, but that 
    want to invest and transform into data-oriented organizations.
* Data accumulated in very heterogeneous sources (relational databases, Big Data infrastructure, cloud infrastructure).

All this causes an increasing complexity when working with data and designing processes for its exploitation:

* It is more complicated and critical to monitor (executions, failures).
* It is more complicated to find bugs and fix them (search the logs, etc.).
* It is more complicated to maintain the processes and introduce changes without affecting critical parts.

Apache Airflow has gained great popularity in the coming years, especially due to the rise of Data projects using Machine 
Learning libraries written in Python or whose main API is in Python, which is becoming the 
[reference language] (https://stackoverflow.blog/2017/09/06/incredible-growth-python/) in the field of data analysis 
and artificial intelligence (sorry R).

If programming languages were divided in terms of their efficiency and
[speed] (http://www.bioinformatics.org/benchmark/results.html) in execution, 
there would be 3 distinct groups:

1. Fast languages: C, C ++, Fortran.
2. Languages with intermediate speed: Java, Scala.
3. Slow languages: Python, Ruby, Perl.

Most of the code written in Python for scientific computing and data analysis, uses under the hood extensions 
in C or C ++ (as in the case of NumPy or Tensorflow). Python does a good job as a wrapper and nexus of
code written in other (faster) languages. At the same time, its learning curve is reduced compared to
other languages, so it attracts users with little experience in programming and software development, but with
solid knowledge about data analytics. Growth in recent years has been exponential.

![Python growth over time](./images/python.png)

## Apache Airflow Introduction

### Airflow Features

Python properties as a 'glue' language fit perfectly with the concept proposed by Apache Airflow, that is why its 
use has increased since its [release](https://airbnb.io/projects/airflow/) by the AirBnB engineering team.

Apache Airflow is defined as:

> A platform to programmatically author, schedule and monitor workflows.

The main features of Apache Airflow are the following:

* Usability
     * Web interface.
     * Creation and use of connections with diverse infrastructure.
     * Review of logs of each task independently.
     * Visualization of the executed code in each task.
* Robustness:
     * Task retry management.
     * Dependency between tasks.
* Elegant:
     * Definition of execution graphs (DAGs) as .py files
     * Minimum knowledge about scripting required.
     
### Airflow operating scheme
     
Airflow consists of 4 main components.

* Webserver:
     * Process monitoring and visualization.
     * Query execution logs.
     * Definition of 'connections'.
* Scheduler:
     * Launching tasks and processes at the right time and order.
* Metadata database:
     * Storage of the status of tasks and processes: queued, running, retrying, finished, failed.
     * Storage of connections, users, passwords, etc.
* Worker (optional):
     * This component is responsible for executing the tasks offering additional functionalities to the execution by 
     default. These additional functionalities usually have to do with the distribution of the execution.
        
### Main components of Apache Airflow workflows

The main components of Apache Airflow are the following:

* DAG: Acronym for Directed Acyclic Graph: it is a set of tasks arranged according to a certain 
dependence between them and that are executed with a certain periodicity.
* Tasks: execution units.
* Operators: define the type of task. They are subdivided into three types:
    * Operators: execute some arbitrary action.
    * Transfers: move information between different locations.
    * Sensors: wait for changes in the system to start the execution.
 * Hooks: communication interfaces with the infrastructure.
 * Plugins: extensions of all the previous elements.
 
### Ways to execute processes in Airflow: executors.

There is a big difference in the way processes are executed in Apache Airflow. The element that performs the execution 
of the end of tasks in Airflow is called executor. There are several types of executors, each with their strengths
and drawbacks:

* Sequential executor: is the default executor of Apache Airflow. It is characterized by executing tasks sequentially 
(without any parallelization). It is good for prototyping processes and developing.
* Local executor: uses Python built-in multiprocessing library. Its great advantage is that it does not require any 
external elements to work and supports parallelization of tasks in a local machine. It is a good option when airflow 
tasks needs some processing power and scheduler is on a single computer.
* [Celery](http://www.celeryproject.org/) executor: Celery is by definition a distributed task queue. Its
main feature is that it allows to distribute the tasks by several machines that are coordinated with the help of a 
broker like Redis or RabbitMQ.
* [Dask](https://dask.org/) executor: Dask has been one of the great revelations in the analytical community that allow 
to distribute Python natively. Its main feature is that beyond distributing tasks by certain components of a cluster, 
Dask distributes the tasks themselves, using distributed arrays of pandas and numpy. Please note the difference between
distributing tasks and distributed tasks.

## Apache Airflow setup

### Step 1: Apache Airflow installation in a virtual environment

It is recommended to install Airflow in a conda virtual environment, along with the rest of the dependencies
of this session. Miniconda is already installed in the virtual machine provided. For more information about
conda virtual environment manager, it is recommended to read the following content:

* https://medium.freecodecamp.org/why-you-need-python-environments-and-how-to-manage-them-with-conda-85f155f4353c
* https://conda.io/docs/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file

A conda environment file `.yml`, include the necessary requirements for the creation of an environment, these, the 
libraries which is necessary to install. An example of a .yml file would be the following:

```yml
name: airflow_env
channels:
  - default
dependencies:
  - pip:
    - apache-airflow[postgres]
```

To create this environment execute the following commands:

* `sudo apt install gcc`
* `conda env create -f /path/to/env_file.yml`

There are several ways to install Apache Airflow depending on the integrations that will be used. In this workshop we will install 
Airflow base and the libraries needed for the integration of Airflow with Postgres. For more information about Airflow installation 
options, please check the docs:

* http://airflow.apache.org/installation.html

The way of installing Airflow differs depending on whether it is done using the Python default package manager (pip)
or the Anaconda environment manager (conda). Depending on the installed version, the installation of additional libraries
will have to be performed or not. Usually, conda installation could be defined as more 'automatic', performing a more detailed 
management of the dependencies, and installing `gcc` automatically.

### Step 2. Database init (for metadata)

Once the setup of all requirements has been completed, a database for the Airflow metadata (graphs, tasks, connections, 
execution status, statistics, etc.) must be initialized.

Airflow is able to use a large number of technologies as database backend. The choice of such 
technology has profound implications in what Apache Airflow can do:

* SQLite: used by default. Creates a `.db` file where you store the metadata, without any other additional requirement 
it has the drawback of not allowing parallel task execution (because of the `.db` file does not support concurrent connections).
* Postgres, MySQL, and other enterprise databases: allow parallel task execution (allows connection concurrency).

In this practical session, SQLite will be used for initial testing, later on, we will setup Postgres. Postgres is already installed 
on the Virtual Machine provided, in case of not having an installation of Postgres, install it by running the following commands:

* `sudo apt update`
* `sudo apt install postgresql postgresql-contrib pgadmin3`

To initialize the metadata using the default backend (SQLite), the Python virtual environment must first be activated, using the 
following command:

* `conda activate airflow_env`

Once the environment is activated, the prompt will change and show the name of the environment in parentheses. All actions 
performed (installation of libraries) will be carried out on said environment.

To initialize the metadata database, the following command must be executed with the environment activated:

* `airflow initdb`

By default, the directory `~/airflow/` will be created and inside it there will be a file called `airflow.db` that, the 
SQLite database that contains the metadata. The internal structure can be obtained by connecting programmatically with 
the database (for example with the standard Python sqlite module) or with a SQLite viewer as DB Browser for SQLite, 
DBeaver or a commercial tool like JetBrains DataGrip.

**Note**: The location of the airflow folder can be modified by setting the `AIRFLOW_HOME` environment variable
before the initialization of the metadata.

### Step 3. Boot the web server and scheduler

Once the database has been initialized, the installation is complete and only remains to activate each of the
Airflow components:

- webserver

    To activate the web server (optionally it can be launched on screen or tmux, making sure that the environment is
     deactivated at the time of the creation of the multiplexer session):
     
     * `tmux new -s airflow_webserver` (optional)
     * `conda activate airflow_env`
     * `airflow webserver`
     
    To exit tmux session and leave the web server running in the background, press `ctrl + b` and then just the
    `d` key.

- scheduler

    The process for the scheduler is repeated:
    
     * `tmux new -s airflow_scheduler` (optional)
     * `conda activate airflow_env`
     * `airflow scheduler`
 
Once the web server and scheduler have been started, the Apache Airflow web interface can be accessed at the URL 
(by default, it can be modified by adding the ip and port options in the launch command):

* `http: // localhost: 8080`

![Apache Airflow Web Interface](./images/dag_list.png)

## Airflow tuning beyond boilerplate

### Parallel task execution

In this section, some of the Airflow configuration options will be modified to:

* Allow the execution of tasks in parallel.
* Optimize the use of system resources on limited resources (such as the virtual machine) and shared environments.

Both the web server and the scheduler must be stopped. To access the scheduler execution terminal in case
If it has been launched on tmux, execute:

* `tmux attach -t airflow_webserver`
* Press `ctrl + c` to stop the process
* Repeat the process for scheduler

Next, you have to create a postgres database that will be used by Airflow for the storage of metadata. Postgres must be 
already installed in the virtual machine, you can use pgAdminIII to create the user and database, but we will cover the
process using psql cli:

1. Switch to postgres user: `sudo su postgres` (introduce your password).
2. You will access psql, the command line application to manage Postgres on the computer: `psql`.
3. Execute the following query: `CREATE USER airflow WITH ENCRYPTED PASSWORD 'airflow';`
4. Create airflow database: `CREATE DATABASE airflow;`
5. Give permissions to airflow user in airflow database: `GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;`
6. Quit psql with `\q`.

Once the database has been created, the Airflow backend must be modified in the config file, so that it
 start using this new database instead of the one used by default (SQLite).

The config file is located in `~/airflow/airflow.cfg`, around line 40 there is the option to specify the metadata 
database:

```ini
# The SqlAlchemy connection string to the metadata database.
# SqlAlchemy supports many different database engine, more information
# their website
sql_alchemy_conn = sqlite:////home/<user>/airflow/airflow.db
```

The SQLite database is currently configured, which is nothing more than a local file called airflow.db in the
`~/airflow` folder. To use the postgres database that has just been created, the connection string must be replaced 
with:

```ini
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@localhost:5432/airflow
```

The config file is then saved and the new database is initialized again (remember activating conda virtual env first):

* `airflow initdb`

So that Airflow support parallel execution of tasks that have no dependence on each other, in addition to
provide a backend that supports concurrent writing, you must select a type of executor that supports this
characteristic. You can choose several types of executors:

Other advanced options like:

* Sequential: it is a type of executor that executes the tasks sequentially, one after another. Ideal for prototyping 
and making tests.
* Local: basic executor that supports parallel execution using multiprocessing.

Advanced options like:

* Celery: use Celery executors, requiring a broker, such as RabbitMQ or Redis, to distribute the tasks
Among the executors. This configuration is more advanced and goes beyond the scope of this workshop.
* Dask: uses executors of [Dask](https://dask.pydata.org/en/latest/), a framework that provides distribution of 
analytical tasks with an API very similar to pandas, numpy, etc. This setting is more advanced and out of the scope of 
this workshop.

To use the Local type executor, the configuration file around line #35 must be modified:

```ini
# The executor class that airflow should use. Choices include
# SequentialExecutor, LocalExecutor, CeleryExecutor, DaskExecutor
executor = SequentialExecutor
```

Line 35 must be replaced by the following:

* `executor = LocalExecutor`

### Improve performance in shared & low resources environments

In this section a series of changes will be made to improve the performance of Airflow in the virtual machine and 
computers with limited resources.

The following options will be modified in the configuration:

* `parallelism` (~line 54): number of tasks marked as active in the database at the same time. It will be reduced to 8.
* `dag concurrency` (~line 57): number of active tasks per worker (in the case of a basic local executor there will 
only be one worker). It will be reduced to 4.
* `max_active_runs_per_dag` (~line 67): number of times the same DAG can be active. It will be reduced to 2.
* `max_threads` (~line 333): the number of processes that the scheduler can start. Allows control directly on the cpu. 
It must match the number of processor cores. In this case, it will be set to 2.
* `min_file_process_interval` (~line 298): time interval with which files are read in the dags folder. By default they 
are read continuously (0 option). It will be set to 60 to read every minute.
* `dagbag_import_timeout` (~ line 84): the time after which a timeout error is raised when reading the dags. Will be 
fixed in 60.

### Setup Airflow as a system service

To setup Airflow as a service using systemd (__mandatory__ in production environments), create the following files in 
`/etc/systemd/system/` path.

* Scheduler

    ```
    [Unit]
    Description=Airflow scheduler
    After=network.target
    
    [Service]
    Environment=AIRFLOW_HOME=/home/user/airflow
    Restart=on-failure
    RestartSec=30
    StandardOutput=file:/var/log/airflow/scheduler/stdout.log
    StandardError=file:/var/log/airflow/scheduler/stderr.log
    ExecStart=/bin/bash -c 'PATH=/home/user/miniconda3/envs/airflow_env/bin/:$PATH exec airflow scheduler'
    
    [Install]
    WantedBy=multi-user.target
    ```

* Webserver

    ```
    [Unit]
    Description=Airflow webserver
    After=network.target
    
    [Service]
    Environment=AIRFLOW_HOME=/home/user/airflow
    Restart=on-failure
    RestartSec=30
    StandardOutput=file:/var/log/airflow/webserver/stdout.log
    StandardError=file:/var/log/airflow/webserver/stderr.log
    ExecStart=/bin/bash -c 'PATH=/home/user/miniconda3/envs/airflow_env/bin/:$PATH exec airflow webserver'
    
    [Install]
    WantedBy=multi-user.target
    ```
