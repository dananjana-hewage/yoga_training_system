from flask import Flask, jsonify
import mysql.connector

app =Flask(__name__)

con=mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    password= 'Swix@7466',
    database = 'yoga_project'
)

@app.route('/getTable',methods=['GET'])
def get_tables():
    cursor=con.cursor()
    cursor.execute("SHOW TABLES;")
    tables=cursor.fetchall()
    cursor.close()
    con.close()
    print (tables)
    table_names= [table[0] for table in tables]
    return jsonify({"tables":table_names}),200

if __name__=="__main__":
    print("connecting to DB...")
    app.run(debug=True)