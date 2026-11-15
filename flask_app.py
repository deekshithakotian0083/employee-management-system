"""Minimal Flask web app for the Employee Management System."""

from flask import Flask, jsonify

from app import EmployeeManagementSystem

flask_app = Flask(__name__)
ems = EmployeeManagementSystem()


@flask_app.route("/")
def index():
    return jsonify(message="Employee Management System is running")


@flask_app.route("/health")
def health():
    return jsonify(status="ok")


@flask_app.route("/employees")
def employees():
    return jsonify(ems.list_employees())


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000)
