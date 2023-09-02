import json
import requests
import pendulum
import logging
from airflow.operators.python import get_current_context
from airflow.decorators import dag, task


def upsert_mysql(timestamp: int, article: str, views: int):
    # Establish a connection to MySQL
    import mysql
    import mysql.connector
    connection = mysql.connector.connect(
        host="hahattpro-dev-mysql-hahattpro-041c.aivencloud.com",
        port="18357",
        user="avnadmin",
        password="AVNS_XmS6WtCl2BzqZCOF6Dn",
        database="defaultdb"
        
    )



    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query for upsert
    sql = """
    INSERT INTO pageview (timestamp, article, views)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE views = views
    """

    # Execute the upsert query
    cursor.execute(sql, (timestamp, article, views))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the connection
    cursor.close()
    connection.close()


list_of_tracked_wiki = [
    "Cthulhu_Mythos",
    "Cthulhu_Mythos_deities",
    "Elder_God_(Cthulhu_Mythos)",
    "Ghatanothoa",
    "Nyarlathotep",
    "Azathoth",
    "Cult_(religious_practice)",
    "Cthulhu",
    "Wikiwand",
    "Company_scrip",
    "At_the_Mountains_of_Madness",
    "Weird_Tales",
    "Panties"
]


def upsert_postgresql(timestamp: int, article: str, views: int):
    import psycopg2
    # Establish a connection to PostgreSQL
    connection = psycopg2.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_database"
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query for upsert
    sql = """
    INSERT INTO your_table (timestamp, article, views)
    VALUES (%s, %s, %s)
    ON CONFLICT (timestamp) DO UPDATE SET views = your_table.views + %s
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
    start_date=pendulum.datetime(2023, 3, 1, tz="UTC"),
    end_date=pendulum.datetime(2023, 4, 1, tz="UTC"),
    catchup=True,
    tags=["wiki"]
)
def wiki_pageview_dag_extends():
    

    @task 
    def call_api(page_name):
        context = get_current_context()
        ds_nodash = context.get("ds_nodash")
        # example: https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/desktop/user/Cthulhu_Mythos/daily/20230801/20230801
        base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/desktop/user"
        url = f"{base_url}/{page_name}/daily/{ds_nodash}/{ ds_nodash }"
        headers = {
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "User-Agent": "Meow I am pusheen the cat. Meow.",
            "accept": "application/json"
        }
        
        logging.info(url)
        r = requests.get(url, headers=headers)
        
        obj = r.json()
        logging.info(json.dumps(obj))
        return json.dumps(obj)
    
    @task 
    def ingest_mysql(obj_str):
        logging.info("object str is " + obj_str)
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

    output_list = call_api.expand(page_name=list_of_tracked_wiki)
    ingest_mysql.expand(obj_str=output_list)
    
    # output1 = call_api("Let_the_Right_One_In_(novel)")
    # output2 = call_api("Gothic_fiction")
    # ingest_mysql(output1)
    # ingest_mysql(output2)

wiki_pageview_dag_extends()