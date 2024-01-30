import mysql
import mysql.connector
import json
import logging
import requests

def upsert_mysql(timestamp: int, article: str, views: int):
    # Establish a connection to MySQL
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port="7777",
        user="root",
        password="meowmeow",
        database="defaultdb"
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

def call_api(page_name):
    
    ds_nodash = "20231112"
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

def ingest_mysql(obj_str):
    obj = json.loads(obj_str)
    items = obj["items"]
    for it in items:
        article = it["article"]
        timestamp = it["timestamp"]
        views = it["views"]
        upsert_mysql(timestamp, article, views)

if __name__ == "__main__":
    obj = call_api("Cthulhu_Mythos")
    print(obj)
    ingest_mysql(obj)
