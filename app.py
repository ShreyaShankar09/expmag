from flask import Flask, jsonify, request, url_for
from werkzeug.exceptions import BadRequest


app = Flask(__name__)
app.config["EMPLOYEES"] = {}
app.config["NEXT_EMPLOYEE_ID"] = 1


@app.get("/api/health")
def health():
    return jsonify(status="ok")


@app.get("/api/employees")
def get_employees():
    return jsonify(list(app.config["EMPLOYEES"].values()))


@app.get("/api/employees/<int:employee_id>")
def get_employee(employee_id):
    employee = app.config["EMPLOYEES"].get(employee_id)
    if employee is None:
        return jsonify(error="Employee not found"), 404

    return jsonify(employee)


@app.post("/api/employees")
def create_employee():
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 415

    try:
        data = request.get_json()
    except BadRequest:
        return jsonify(error="Request body must be valid JSON"), 400

    if not isinstance(data, dict):
        return jsonify(error="Request body must be a JSON object"), 400

    required_fields = ("name", "email", "department")
    if any(
        not isinstance(data.get(field), str) or not data[field].strip()
        for field in required_fields
    ):
        return jsonify(
            error="name, email, and department are required non-empty strings"
        ), 400

    employee_id = app.config["NEXT_EMPLOYEE_ID"]
    employee = {
        "id": employee_id,
        "name": data["name"].strip(),
        "email": data["email"].strip(),
        "department": data["department"].strip(),
    }
    app.config["EMPLOYEES"][employee_id] = employee
    app.config["NEXT_EMPLOYEE_ID"] = employee_id + 1

    return (
        jsonify(employee),
        201,
        {"Location": url_for("get_employee", employee_id=employee_id)},
    )


if __name__ == "__main__":
    app.run()