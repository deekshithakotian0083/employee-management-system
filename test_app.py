"""Unit tests for the Employee Management System."""

import unittest
from app import EmployeeManagementSystem


class TestEmployeeManagementSystem(unittest.TestCase):
    def setUp(self):
        self.system = EmployeeManagementSystem()

    def add_sample_employee(self):
        return self.system.add_employee(
            "E001", "Asha Rao", "Engineering", "Python Developer", 45000
        )

    def test_add_employee(self):
        employee = self.add_sample_employee()
        self.assertEqual(employee["employee_id"], "E001")
        self.assertEqual(employee["name"], "Asha Rao")
        self.assertEqual(employee["salary"], 45000.0)

    def test_list_employees(self):
        self.add_sample_employee()
        self.system.add_employee("E002", "Ravi Kumar", "HR", "HR Executive", 35000)
        self.assertEqual(len(self.system.list_employees()), 2)

    def test_search_employee(self):
        self.add_sample_employee()
        self.assertEqual(self.system.get_employee("E001")["department"], "Engineering")

    def test_update_employee(self):
        self.add_sample_employee()
        updated = self.system.update_employee("E001", designation="Senior Developer")
        self.assertEqual(updated["designation"], "Senior Developer")

    def test_delete_employee(self):
        self.add_sample_employee()
        self.assertTrue(self.system.delete_employee("E001"))
        self.assertEqual(self.system.list_employees(), [])

    def test_duplicate_id_is_rejected(self):
        self.add_sample_employee()
        with self.assertRaises(ValueError):
            self.add_sample_employee()

    def test_blank_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.system.add_employee("E002", " ", "HR", "Recruiter", 30000)

    def test_non_positive_salary_is_rejected(self):
        with self.assertRaises(ValueError):
            self.system.add_employee("E002", "Ravi", "HR", "Recruiter", 0)

    def test_missing_employee_is_rejected(self):
        with self.assertRaises(KeyError):
            self.system.get_employee("E999")


if __name__ == "__main__":
    unittest.main(verbosity=2)
