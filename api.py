from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "accidentdatabase"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

#create/get
@app.route("/accident", methods=["GET"])
def get_accident():
    data = data_fetch("""select * from accident""")
    return make_response(jsonify(data), 200)

#get by id
@app.route("/accident/<int:id>", methods=["GET"])
def get_accidentLocation_by_id(id):
    data = data_fetch("""SELECT * FROM accident where accidentID = {}""".format(id))
    return make_response(jsonify(data), 200)

#inner join
@app.route("/employee/<int:id>/accident", methods=["GET"])
def get__by_employee(id):
    data = data_fetch(
        """
SELECT 
    employee.employeeName, 
    employee.employeeDepartment, 
    accident.accidentDescription, 
    accident.accidentDate, 
    accident.accidentLocation 
FROM 
    employee 
INNER JOIN 
    accident 
ON 
    employee.employeeID = accident.employee_employeeID 
where 
	employee.employeeID = {}
    """.format(id)
    )
    return make_response(
        jsonify({"employeeID": id, "count": len(data), "accident": data}), 200)

#add
@app.route("/employee", methods=["POST"])
def add_employee():
    cur = mysql.connection.cursor()
    info = request.get_json()
    employeeID = info["employeeID"]
    employeeDepartment = info["employeeDepartment"]
    employeeName = info["employeeName"]
    employeeSupervisor = info["employeeSupervisor"]
    employeeDetails = info["employeeDetails"]
    cur.execute(
        """ INSERT INTO employee (employeeID, employeeDepartment, employeeName, employeeSupervisor, employeeDetails) VALUES (%s, %s, %s, %s, %s)""",
        (employeeID, employeeDepartment, employeeName, employeeSupervisor, employeeDetails),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "employee added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

#update
@app.route("/refaccidenttype/<int:id>", methods=["PUT"])
def update_refaccidenttype(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    accidentTypeDescription = info["accidentTypeDescription"]
    cur.execute(
        """ UPDATE refaccidenttype SET accidentTypeDescription = %s WHERE accidentTypeID = %s """,
        (accidentTypeDescription, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "accident type updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

#delete
@app.route("/accident/<int:id>", methods=["DELETE"])
def delete_accident(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM accident where accidentID = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "accident deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

if __name__ == "__main__":
    app.run(debug=True)
