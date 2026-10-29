
pipeline {
    agent any

    options {
        timestamps()
        skipDefaultCheckout(true)
    }

    stages {

        stage('Source Code Checkout') {
            steps {
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

                bat '''
                python -m unittest -v test_app > reports\\test-report.txt 2>&1
                '''

                echo 'Unit tests completed successfully.'
            }
        }

        stage('Package Artifact') {
            steps {
                bat '''
                powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path app.py,test_app.py,requirements.txt,README.md -DestinationPath employee-management-system.zip -Force"
                '''

                archiveArtifacts artifacts: 'employee-management-system.zip,reports/test-report.txt',
                    allowEmptyArchive: false

                echo 'Application package and test report archived successfully.'
            }
        }

        stage('Docker Version Check') {
            steps {
                bat 'where docker'
                bat 'docker --version'
                bat 'docker info'

                echo 'Docker is accessible from Jenkins.'
            }
        }

        stage('Pull Docker Image') {
            steps {
                bat 'docker pull nginx:alpine'

                echo 'Docker image pulled successfully.'
            }
        }

        stage('Verify Docker Image') {
            steps {
                bat 'docker image inspect nginx:alpine'

                echo 'Docker image verified successfully.'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat '''
                docker rm -f employee-nginx-%BUILD_NUMBER% 2>nul
                docker run -d --name employee-nginx-%BUILD_NUMBER% -p 8082:80 nginx:alpine
                '''

                echo 'Nginx container started on port 8082.'
            }
        }

        stage('Verify Container') {
            steps {
                bat '''
                docker ps --filter "name=employee-nginx-%BUILD_NUMBER%" --filter "status=running" --format "{{.Names}}" > container-status.txt

                for %%A in (container-status.txt) do if %%~zA==0 exit /b 1

                echo Container is running successfully.
                '''

                echo 'Container verification completed.'
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
