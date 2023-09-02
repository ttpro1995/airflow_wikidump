import json
import requests
import pendulum
import logging
from airflow.operators.python import get_current_context
from airflow.decorators import dag, task
import mysql
import mysql.connector

def upsert_mysql(timestamp: int, article: str, views: int):
    # Establish a connection to MySQL
    connection = mysql.connector.connect(
        host="db4free.net",
        user="hahattpro",
        password="MiFHCci@4Reb3C4",
        database="hahattpro"
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query for upsert
    sql = """
    INSERT INTO pageview (timestamp, article, views)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE views = views + %s
    """

    # Execute the upsert query
    cursor.execute(sql, (timestamp, article, views, views))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the connection
    cursor.close()
    connection.close()

@dag(
    #schedule=None,
    schedule_interval='@daily',
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    end_date=pendulum.datetime(2022, 1, 2, tz="UTC"),
    catchup=True,
    tags=["wiki"]
)
def wiki_pageview_dag():
    

    @task 
    def call_api(page_name):
        context = get_current_context()
        ds_nodash = context.get("ds_nodash")
        # example: https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/desktop/user/Cthulhu_Mythos/daily/20230801/20230801
        base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/desktop/user"
        url = f"{base_url}/{page_name}/daily/{ds_nodash}/{ ds_nodash }"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        }
        logging.info(url)
        r = requests.get(url, headers=headers)
        
        obj = r.json()
        logging.info(json.dumps(obj))
        return json.dumps(obj)
    
    @task 
    def ingest_mysql(obj_str):
        obj = json.loads(obj_str)
        items = obj["items"]
        for it in items:
            article = it["article"]
            timestamp = it["timestamp"]
            views = it["views"]
            upsert_mysql(timestamp, article, views)

    
    
    @task
    def show(obj):
        print(obj)
        logging.info(obj)

    
    output1 = call_api("Let_the_Right_One_In_(novel)")
    output2 = call_api("Gothic_fiction")
    ingest_mysql(output1)
    ingest_mysql(output2)

wiki_pageview_dag()