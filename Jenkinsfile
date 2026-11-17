
pipeline {
    agent any

    options {
        timestamps()
        skipDefaultCheckout(true)
    }

    stages {

        // Stage 1: Checkout source code from GitHub
        stage('Source Code Checkout') {
            steps {
                checkout scm
                echo 'Source code checkout completed.'
            }
        }

        // Stage 2: Validate Python version and syntax
        stage('Build and Validation') {
            steps {
                bat 'python --version'
                bat 'python -m py_compile app.py test_app.py'

                echo 'Python syntax validation passed.'
            }
        }

        // Stage 3: Execute unit tests
        stage('Test') {
            steps {
                bat 'if not exist reports mkdir reports'

                bat '''
                    python -m unittest -v test_app > reports\\test-report.txt 2>&1
                    if errorlevel 1 exit /b 1
                '''

                echo 'All unit tests passed successfully.'
            }
        }

        // Stage 4: Create and archive application package
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

        // Stage 5: Check Docker installation and connection
        stage('Docker Version Check') {
            steps {
                bat 'docker --version'
                bat 'docker info'

                echo 'Docker is accessible from Jenkins.'
            }
        }

        // Stage 6: Download Nginx Docker image
        stage('Pull Docker Image') {
            steps {
                bat 'docker pull nginx:alpine'

                echo 'Docker image pulled successfully.'
            }
        }

        // Stage 7: Verify downloaded Docker image
        stage('Verify Docker Image') {
            steps {
                bat 'docker image inspect nginx:alpine'

                echo 'Docker image verified successfully.'
            }
        }

        // Stage 8: Create and start Nginx container
        stage('Run Docker Container') {
            steps {
                bat '''
                    docker rm -f employee-nginx 2>nul
                    docker run -d --name employee-nginx -p 8083:80 nginx:alpine
                '''

                echo 'Nginx container started on port 8083.'
            }
        }

        // Stage 9: Verify that the container is running
        stage('Verify Container') {
            steps {
                bat '''
                    docker ps --filter "name=employee-nginx" --filter "status=running" --format "{{.Names}}" > container-status.txt

                    for %%A in (container-status.txt) do if %%~zA==0 exit /b 1

                    echo Container is running successfully.
                '''

                echo 'Container verification completed.'
            }
        }

        // Stage 10: Build the Flask application Docker image
        stage('Build Flask Docker Image') {
            steps {
                bat 'docker build -t jenkins-flask-app:1.0 .'

                echo 'Flask Docker image jenkins-flask-app:1.0 built successfully.'
            }
        }

        // Stage 11: Run the Flask container on port 8082
        stage('Run Flask Container') {
            steps {
                bat '''
                    docker rm -f jenkins-flask-app 2>nul
                    docker run -d --name jenkins-flask-app -p 8082:5000 jenkins-flask-app:1.0
                '''

                echo 'Flask container started on port 8082.'
            }
        }

        // Stage 12: Verify the Flask application responds
        stage('Verify Flask Container') {
            steps {
                bat '''
                    docker ps --filter "name=jenkins-flask-app" --filter "status=running" --format "{{.Names}}" > flask-container-status.txt

                    for %%A in (flask-container-status.txt) do if %%~zA==0 exit /b 1

                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$ok=$false; for ($i=0; $i -lt 10; $i++) { try { if ((Invoke-WebRequest -UseBasicParsing http://localhost:8082/health).StatusCode -eq 200) { $ok=$true; break } } catch { Start-Sleep -Seconds 2 } }; if (-not $ok) { exit 1 }"
                '''

                echo 'Flask application is healthy on port 8082.'
            }
        }
    }

    // Post-build actions
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
