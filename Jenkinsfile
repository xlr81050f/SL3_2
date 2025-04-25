pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh 'python manage.py test'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'echo "Deploying application..."'
                // Add deployment steps here
                // For example: sh 'docker-compose up -d --build'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}