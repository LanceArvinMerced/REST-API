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
@app.route("/employee", methods=["GET"])
def get_employees():
    data = data_fetch("""select * from employee""")
    return make_response(jsonify(data), 200)

#get by id
@app.route("/employee/<int:id>", methods=["GET"])
def get_employeeName_by_id(id):
    data = data_fetch("""SELECT * FROM employee where id = {123}""".format(id))
    return make_response(jsonify(data), 200)

#inner join
@app.route("/employee/<int:accidentID>/accident", methods=["GET"])
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
WHERE 
    employee.employeeID = {};

    """
    .format(accidentID)

    )
    return make_response(
        jsonify({"employee_id": id, "count": len(data), "accident": data}), 200
    )

#add
@app.route("/refaccidenttype", methods=["POST"])
def add_refaccidenttype():
    cur = mysql.connection.cursor()
    info = request.get_json()
    accidentTypeID = info["21"]
    accidentTypeDescription = info["burn"]
    cur.execute(
        """ INSERT INTO actor (first_name, last_name) VALUE (%s, %s)""",
        (accidentTypeID, accidentTypeDescription),
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
@app.route("/actors/<int:id>", methods=["PUT"])
def update_actor(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    first_name = info["first_name"]
    last_name = info["last_name"]
    cur.execute(
        """ UPDATE actor SET first_name = %s, last_name = %s WHERE actor_id = %s """,
        (first_name, last_name, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "actor updated successfully", "rows_affected": rows_affected}
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
