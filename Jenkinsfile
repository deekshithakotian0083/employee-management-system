pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Source Code Checkout') {
            steps {
                // For a Pipeline script loaded from SCM or a Multibranch Pipeline.
                checkout scm
                echo 'Source code checkout completed.'
            }
        }

        stage('Build and Validation') {
            steps {
                bat 'python --version'
                bat 'python -m py_compile app.py test_app.py'
                echo 'Python syntax validation passed.'
            }
        }

        stage('Test') {
            steps {
                bat 'if not exist reports mkdir reports'
                // Capture test output while preserving the test command's exit code.
                bat 'python -m unittest -v test_app > reports\\test-report.txt 2>&1'
            }
        }

        stage('Package Artifact') {
            steps {
                bat 'powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path app.py,test_app.py,requirements.txt,README.md -DestinationPath employee-management-system.zip -Force"'
                archiveArtifacts artifacts: 'employee-management-system.zip,reports/test-report.txt',
                    allowEmptyArchive: false
            }
        }
    }

    post {
        success {
            echo 'Employee Management System CI pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Review the stage logs and test report.'
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
