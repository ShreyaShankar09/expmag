from flask import Flask, jsonify, request


app = Flask(__name__)


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


@app.post("/api/echo")
def echo():
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 415

    return jsonify(received=request.get_json())


if __name__ == "__main__":
    app.run()