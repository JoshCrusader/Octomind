import MySQLdb


# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
def pull_data():
    data_return = []
    host = "192.168.1.4"
    connection = MySQLdb.connect(
        host=host,
        user="root",
        passwd="root",
        db="sensorDB")

    # prepare a cursor object using cursor() method
    cursor = connection.cursor()

    # execute the SQL query using execute() method.
    cursor.execute("select * from sensor_log")

    # fetch all of the rows from the query
    data = cursor.fetchall()

    # print the rows
    for row in data:
        data_return.append({"log_id": row[0], "timestamp": row[1], "sensor_id": row[2], "value": row[3]})
    # close the cursor object
    cursor.close()
    # close the connection
    connection.close()

    return data_return

