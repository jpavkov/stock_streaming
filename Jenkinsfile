pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                // Pull the latest code from GitHub
                git url: 'https://github.com/jpavkov/stock_streaming.git', branch: 'main'
            }
        }

        stage('Setup Environment') {
            steps {
                // Ensure the virtual environment is set up
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate'

                // Install dependencies
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Application') {
            steps {
                // Run your application script
                sh 'source venv/bin/activate && python src/main.py'
            }
        }

        stage('Build') {
            steps {
                // Build the Docker image
                sh 'docker build -t jpavkov/stock_streaming:latest .'
            }
        }

        stage('Deploy') {
            steps {
                // Load environment variables from .env file
                sh 'set -o allexport; source .env; set +o allexport'

                // Log in to Docker Hub
                sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'

                // Push the Docker image to Docker Hub
                sh 'docker push jpavkov/stock_streaming:latest'

                // Optional: Run the Docker container (if applicable)
                // sh 'docker run -d -p 8080:8080 jpavkov/stock_streaming:latest'
            }
        }
    }
}
