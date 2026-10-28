# Employee Management System

A small Python console application for managing employee records, created as a Jenkins CI/CD practice project.

## Features

- Add an employee
- List all employees
- Search by employee ID
- Update employee details
- Delete an employee
- Validate required fields, duplicate IDs, and positive salaries

## Technology

- Python 3
- `unittest` for automated tests
- Git and GitHub for version control
- Jenkins Pipeline for CI/CD
- PowerShell `Compress-Archive` for packaging on Windows

The application stores records in memory. Employee records are cleared when the application exits; this practice version does not use a database.

## Prerequisites

- Python 3 installed on the machine running Jenkins
- Git installed and available to Jenkins
- Jenkins with the Git and Pipeline plugins
- A Git repository containing this project

No third-party Python packages are required.

## Run locally on Windows

Open Command Prompt or PowerShell in this directory:

```powershell
python app.py
```

## Run automated tests

```powershell
python -m unittest -v test_app
```

## Validate Python syntax

```powershell
python -m py_compile app.py test_app.py
```

## Jenkins setup

1. Commit and push this project to a Git repository.
2. In Jenkins, create a Pipeline job or Multibranch Pipeline.
3. For a Pipeline job, select **Pipeline script from SCM**, choose **Git**, enter the repository URL and branch, and set Script Path to `Jenkinsfile`.
4. Ensure the Windows Jenkins agent can run `python`, `git`, and PowerShell.
5. Save and run the job.

The Jenkinsfile checks out the code, validates syntax, runs unit tests, creates a test report, packages the project into a ZIP file, and archives the report and ZIP artifact.

The provided `checkout scm` step is intended for a pipeline configured from source control. If using a Pipeline script pasted directly into Jenkins, configure the repository URL and branch explicitly instead.

## Demonstrating failure and recovery

1. Run the pipeline with the original tests and confirm a successful result.
2. For a controlled failure, temporarily change the expected result in `test_app.py`, for example change `self.assertEqual(add(2, 3), 5)` only if such a test exists, or change an existing employee assertion to an incorrect expected value.
3. Commit and push the intentional test change, then run the pipeline and capture the failed test output.
4. Restore the correct expected value, commit and push the fix, and rerun.
5. Capture the successful run and archived artifacts.

Do not leave the intentional failing test in the final version.

## Credentials

This public-repository practice project does not need application secrets. If the repository is private, configure repository credentials in Jenkins Credentials rather than storing tokens or passwords in the Jenkinsfile.
