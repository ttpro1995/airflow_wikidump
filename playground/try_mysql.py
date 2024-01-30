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
    ON DUPLICATE KEY UPDATE views = views + %s
    """

    # Execute the upsert query
    cursor.execute(sql, (timestamp, article, views, views))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the connection
    cursor.close()
    connection.close()

upsert_mysql(2023010100, "test", 1000)