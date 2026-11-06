import unittest

from app import app


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        app.config["EMPLOYEES"] = {}
        app.config["NEXT_EMPLOYEE_ID"] = 1
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_get_employees_returns_empty_list(self):
        response = self.client.get("/api/employees")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_employee_returns_not_found_for_unknown_id(self):
        response = self.client.get("/api/employees/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Employee not found"})

    def test_echo_endpoint_accepts_json(self):
        payload = {"name": "Ada", "role": "developer"}

        response = self.client.post("/api/echo", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"received": payload})

    def test_echo_endpoint_rejects_non_json(self):
        response = self.client.post("/api/echo", data="not json")

        self.assertEqual(response.status_code, 415)
        self.assertEqual(
            response.get_json(),
            {"error": "Content-Type must be application/json"},
        )


if __name__ == "__main__":
    unittest.main()
