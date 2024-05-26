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


def data_fetch(query):
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
	employee.employeeID = 123
    """.format(id)
    )
    return make_response(
        jsonify({"employeeID": id, "count": len(data), "accident": data}), 200)

#add
@app.route("/employees", methods=["POST"])
def add_employee():
    cur = mysql.connection.cursor()
    info = request.get_json()
    employeeID = info["employeeID"]
    employeeDepartment = info["employeeDepartment"]
    employeeName = info["employeeName"]
    employeeSupervisor = info["employeeSupervisor"]
    employeeDetails = info["employeeDetails"]
    cur.execute(
        """ INSERT INTO employee (employeeID, employeeDepartment, employeeName, employeeSupervisor, employeeDetails) VALUE (%s, %s, %s, %s, %s)""",
        (employeeID, employeeDepartment, employeeName, employeeSupervisor, employeeDetails),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "actor added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

#update
@app.route("/refaccidenttype/<int:id>", methods=["PUT"])
def update_actor(id):
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
            {"message": "actor   updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

#delete
@app.route("/actors/<int:id>", methods=["DELETE"])
def delete_actor(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM actor where actor_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "actor deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

#uri
@app.route("/actors/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)

if __name__ == "__main__":
    app.run(debug=True)
