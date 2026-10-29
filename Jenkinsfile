
        stage('Docker Version Check') {
            steps {
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
                docker run -d --name employee-nginx-%BUILD_NUMBER% -p 8081:80 nginx:alpine
                '''
                echo 'Nginx container started.'
            }
        }

        stage('Verify Container') {
            steps {
                bat '''
                docker ps --filter "name=employee-nginx-%BUILD_NUMBER%" --filter "status=running" --format "{{.Names}}" > container-status.txt

                for %%A in (container-status.txt) do if %%~zA==0 exit /b 1

                echo Container is running successfully.
                '''
            }
        }