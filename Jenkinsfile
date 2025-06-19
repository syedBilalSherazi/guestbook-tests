pipeline {
    agent any

    environment {
        IMAGE_NAME      = "guestbook-tests-image"
        CONTAINER_NAME  = "guestbook-tests-container"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh "docker build -t $IMAGE_NAME ."
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo "Running tests in container..."
                // Clean up if a container already exists
                sh "docker rm -f $CONTAINER_NAME || true"
                // Run the test container
                sh "docker run --name $CONTAINER_NAME $IMAGE_NAME"
            }
        }
    }

    post {
        success {
            echo 'All tests passed!'
            mail to: 'syedbilalsherazi1004@gmail.com',
                 subject: "✅ Build #${env.BUILD_NUMBER} succeeded in ${env.JOB_NAME}",
                 body: """\
Hello Bilal,

Your build #${env.BUILD_NUMBER} in job '${env.JOB_NAME}' has passed all Selenium tests successfully.

You can view the build details here:
${env.BUILD_URL}

— Jenkins
"""
        }

        failure {
            echo 'One or more tests failed.'
            mail to: 'syedbilalsherazi1004@gmail.com',
                 subject: "❌ Build #${env.BUILD_NUMBER} failed in ${env.JOB_NAME}",
                 body: """\
Hello Bilal,

Your build #${env.BUILD_NUMBER} in job '${env.JOB_NAME}' has failed during Selenium tests.

Check the console output here:
${env.BUILD_URL}console

— Jenkins
"""
        }

        always {
            echo "Cleaning up container if it exists..."
            sh "docker rm -f $CONTAINER_NAME || true"
        }
    }
}
