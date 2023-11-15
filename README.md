# Where is repo ?

https://github.com/ttpro1995/airflow_wikidump

# Run airflow in offline mode

## First time setup
We only need to do once for each project

We set environment variable to project folder

```
export AIRFLOW_HOME=/home/lap60728/workspace/study/airflow_wikidump
export AIRFLOW__CORE__LOAD_EXAMPLES=False 
```
better yet, put it in .env
```
source .env
```

Then run init in same terminal. The environment variable above must be set succesfully 

```
airflow db init # run once
```

# Create first user
```
airflow users create --username meow --password meow --firstname Anonymous --lastname Admin --role Admin --email admin@example.org
```

# Run airflow 

To run airflow, open two separate terminal. Each terminal have to set AIRFLOW_HOME variable.  

```
airflow webserver
```

Then 

```
airflow scheduler
```


# Free mysql

https://console.aiven.io/

# docker sql

```
sudo docker run -d -p 7777:3306 --name airflow_wikidump_sqlserver -e MYSQL_ROOT_PASSWORD=meowmeow mysql:8.2
```
