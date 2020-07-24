#The necessary libraries including the flask library were called to create the REST interface and also the pscopg2 library to connect to the database

import sys
import psycopg2 as ps
from flask import Flask, jsonify , request

#Create a REST interface

app = Flask(__name__)

#Default route to 127.0.0.1:300

@app.route('/')
def home():
    return "<h1 style="color:red;"> Hello Data Science  </h1>"

#We create a GET type function that returns the number of data from the database depending on the conditions, and jsonify was used to make the response be in JSON format.

@app.route('/get_data_count', methods=['GET'])

def get_data_count():
    try:
        connection = ps.connect(user="postgres", password="19980524", host="127.0.0.1", port="5432", database="employees_database")
        cursor = connection.cursor()
        before_date‬‬ = str(request.args.get('‫‪before_date‬‬'))
        count = int(request.args.get('count', default=50000))
        cursor.execute("SELECT id, text  FROM data_input WHERE id <= %s AND date_inter_text < %s", [count, before_date‬‬])
        res_0 = cursor.rowcount
        return jsonify(res_0)
    except:
        return "========>>>Sorry, there is an error in your input!!!!!!!!!!!!!<<<========"
#We create a GET type function that retrieves all texts with a specific classification from the database depending on conditions, and jsonify was used to make the response be in JSON format.

@app.route('/get_data', methods=['GET'])

def get_data():
    try:
        connection =ps.connect(user="postgres", password="19980524", host="127.0.0.1", port="5432", database="employees_database")
        cursor = connection.cursor()
        ‫‪label‬‬ = str(request.args.get('‫‪label‬‬'))
        sort_order = str(request.args.get('sort_order'))
        if(label == 'positive'):
            if (sort_order == 'ascending'):
                res_1 = cursor.execute("SELECT text , label_id FROM data_input INNER JOIN data_labeling  ON id= text_id WHERE label_id = 1 ORDER BY date_inter_text ASC").fetchall()
            elif(sort_order == 'descending'):
                res_1 = cursor.execute("SELECT text , label_id FROM data_input INNER JOIN data_labeling  ON id= text_id WHERE label_id = 1 ORDER BY date_inter_text DESC").fetchall()
        elif(label == 'negative'):
            if (sort_order == 'ascending'):
                res_1 = cursor.execute("SELECT text , label_id FROM data_input INNER JOIN data_labeling  ON id= text_id WHERE label_id = 0 ORDER BY date_inter_text ASC").fetchall()
            elif(sort_order == 'descending'):
                res_1 = cursor.execute("SELECT text , label_id FROM data_input INNER JOIN data_labeling  ON id= text_id WHERE label_id = 0 ORDER BY date_inter_text DESC").fetchall()
        else:
            if (sort_order == 'ascending'):
                res_1 = cursor.execute("SELECT text , label_id FROM data_input INNER JOIN data_labeling  ON id= text_id WHERE label_id = 2 ORDER BY date_inter_text ASC").fetchall()
            elif(sort_order == 'descending'):
                res_1 = cursor.execute("SELECT text , label_id FROM data_input INNER JOIN data_labeling  ON id= text_id WHERE label_id = 2 ORDER BY date_inter_text DESC").fetchall()
        
        return jsonify(res_1)
    except:
        return "========>>>Sorry, there is an error in your input!!!!!!!!!!!!!<<<========"

#Start database_service.py on port 3000
if __name__ == "__main__":
     app.run(debug=True, port=3000)