pipeline {
    agent {
        docker {
            image 'zenika/python-chrome'  // Prebuilt image with Python, Chrome, and ChromeDriver
        }
    }

    environment {
        PYTHONUNBUFFERED = 1
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh 'pytest'
            }
        }
    }

    post {
        always {
            echo 'Test execution completed.'
        }
    }
}
