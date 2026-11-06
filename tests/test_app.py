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

    def test_post_employee_creates_employee(self):
        payload = {
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "department": "Engineering",
        }

        response = self.client.post("/api/employees", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {"id": 1, **payload},
        )
        self.assertEqual(response.headers["Location"], "/api/employees/1")

    def test_post_employee_rejects_non_json(self):
        response = self.client.post("/api/employees", data="not json")

        self.assertEqual(response.status_code, 415)
        self.assertEqual(
            response.get_json(),
            {"error": "Content-Type must be application/json"},
        )

    def test_post_employee_rejects_invalid_json(self):
        response = self.client.post(
            "/api/employees",
            data="{invalid json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Request body must be valid JSON"},
        )

    def test_post_employee_requires_all_fields(self):
        response = self.client.post(
            "/api/employees",
            json={"name": "Ada Lovelace", "email": "ada@example.com"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "name, email, and department are required non-empty strings"},
        )

    def test_created_employee_can_be_retrieved(self):
        create_response = self.client.post(
            "/api/employees",
            json={
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "department": "Engineering",
            },
        )
        employee_id = create_response.get_json()["id"]

        response = self.client.get(f"/api/employees/{employee_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), create_response.get_json())

    def test_created_employee_appears_in_employee_list(self):
        payload = {
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "department": "Engineering",
        }
        created = self.client.post("/api/employees", json=payload).get_json()

        response = self.client.get("/api/employees")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [created])


if __name__ == "__main__":
    unittest.main()
