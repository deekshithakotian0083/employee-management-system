"""Simple in-memory Employee Management System."""


class EmployeeManagementSystem:
    def __init__(self):
        self._employees = {}

    def add_employee(self, employee_id, name, department, designation, salary):
        employee_id = self._validate_id(employee_id)
        name = self._validate_text(name, "Name")
        department = self._validate_text(department, "Department")
        designation = self._validate_text(designation, "Designation")
        salary = self._validate_salary(salary)

        if employee_id in self._employees:
            raise ValueError(f"Employee ID '{employee_id}' already exists.")

        employee = {
            "employee_id": employee_id,
            "name": name,
            "department": department,
            "designation": designation,
            "salary": salary,
        }
        self._employees[employee_id] = employee
        return employee.copy()

    def list_employees(self):
        """Return all employees sorted by employee ID."""
        return [employee.copy() for _, employee in sorted(self._employees.items())]

    def get_employee(self, employee_id):
        employee_id = self._validate_id(employee_id)
        if employee_id not in self._employees:
            raise KeyError(f"Employee ID '{employee_id}' was not found.")
        return self._employees[employee_id].copy()

    def update_employee(self, employee_id, **changes):
        employee_id = self._validate_id(employee_id)
        if employee_id not in self._employees:
            raise KeyError(f"Employee ID '{employee_id}' was not found.")

        allowed_fields = {"name", "department", "designation", "salary"}
        unknown_fields = set(changes) - allowed_fields
        if unknown_fields:
            raise ValueError(f"Unsupported fields: {', '.join(sorted(unknown_fields))}")

        updated = self._employees[employee_id].copy()
        for field, value in changes.items():
            if field == "salary":
                updated[field] = self._validate_salary(value)
            else:
                updated[field] = self._validate_text(value, field.capitalize())

        self._employees[employee_id] = updated
        return updated.copy()

    def delete_employee(self, employee_id):
        employee_id = self._validate_id(employee_id)
        if employee_id not in self._employees:
            raise KeyError(f"Employee ID '{employee_id}' was not found.")
        del self._employees[employee_id]
        return True

    @staticmethod
    def _validate_id(employee_id):
        if employee_id is None:
            raise ValueError("Employee ID is required.")
        employee_id = str(employee_id).strip()
        if not employee_id:
            raise ValueError("Employee ID is required.")
        return employee_id

    @staticmethod
    def _validate_text(value, field_name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} is required.")
        return value.strip()

    @staticmethod
    def _validate_salary(salary):
        if isinstance(salary, bool):
            raise ValueError("Salary must be a positive number.")
        try:
            salary = float(salary)
        except (TypeError, ValueError):
            raise ValueError("Salary must be a valid number.") from None
        if salary <= 0:
            raise ValueError("Salary must be greater than zero.")
        return salary


def main():
    system = EmployeeManagementSystem()

    while True:
        print("\n=== Employee Management System ===")
        print("1. Add employee")
        print("2. List employees")
        print("3. Search employee")
        print("4. Update employee")
        print("5. Delete employee")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        try:
            if choice == "1":
                employee = system.add_employee(
                    input("Employee ID: "),
                    input("Name: "),
                    input("Department: "),
                    input("Designation: "),
                    input("Salary: "),
                )
                print(f"Employee added: {employee}")

            elif choice == "2":
                employees = system.list_employees()
                if not employees:
                    print("No employees found.")
                else:
                    for employee in employees:
                        print(employee)

            elif choice == "3":
                print(system.get_employee(input("Employee ID: ")))

            elif choice == "4":
                employee_id = input("Employee ID: ")
                print("Leave a field blank to keep its current value.")
                current = system.get_employee(employee_id)
                changes = {}
                for field in ("name", "department", "designation", "salary"):
                    value = input(f"{field.capitalize()} [{current[field]}]: ").strip()
                    if value:
                        changes[field] = value
                print(f"Employee updated: {system.update_employee(employee_id, **changes)}")

            elif choice == "5":
                system.delete_employee(input("Employee ID: "))
                print("Employee deleted.")

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Choose a number from 1 to 6.")

        except (ValueError, KeyError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
