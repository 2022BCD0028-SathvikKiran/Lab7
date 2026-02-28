pipeline {
    agent any

    environment {
        IMAGE_NAME = '2022bcd0028/sathvik_model:latest' 
        CONTAINER_NAME = 'ml-inference-test-friend'
    }

    stages {
        stage('Pull Image') {
            steps {
                script {
                    echo "Pulling image ${IMAGE_NAME}..."
                    sh "docker pull ${IMAGE_NAME}"
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                    echo "Starting container ${CONTAINER_NAME}..."
                    // Port mapped to 8002 as per their Dockerfile
                    sh "docker run -d --name ${CONTAINER_NAME} -p 8002:8002 ${IMAGE_NAME}"
                }
            }
        }

        stage('Wait for Service Readiness') {
            steps {
                script {
                    echo "Waiting for API to start..."
                    sleep time: 10, unit: 'SECONDS'
                }
            }
        }

        stage('Validate Inference') {
            steps {
                script {
                    echo "Installing Python requests library..."
                    sh "pip install requests --break-system-packages || pip install requests"
                    
                    echo "Running validation script..."
                    sh "python3 test_inference.py"
                }
            }
        }
    }

    post {
        always {
            script {
                echo "Stopping and removing container..."
                sh "docker rm -f ${CONTAINER_NAME} || true"
            }
        }
    }
}