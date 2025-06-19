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
                // clean up any leftover container
                sh "docker rm -f $CONTAINER_NAME || true"
                // run tests (container’s default CMD is `pytest test_guestbook.py`)
                sh "docker run --name $CONTAINER_NAME $IMAGE_NAME"
            }
        }
    }

    post {
        success {
            echo 'All tests passed!'
            mail to: "${env.GIT_COMMITTER_EMAIL}",
                 subject: "✅ Build #${env.BUILD_NUMBER} succeeded in ${env.JOB_NAME}",
                 body: """\
Hello,

Your recent commit (${env.GIT_COMMIT_ID ?: 'unknown'}) in job ${env.JOB_NAME} passed all Selenium tests.

See build details: ${env.BUILD_URL}

— Jenkins"""
        }

        failure {
            echo 'One or more tests failed.'
            mail to: "${env.GIT_COMMITTER_EMAIL}",
                 subject: "❌ Build #${env.BUILD_NUMBER} failed in ${env.JOB_NAME}",
                 body: """\
Hello,

Your recent commit (${env.GIT_COMMIT_ID ?: 'unknown'}) in job ${env.JOB_NAME} has failed the Selenium tests.

Please review the console output: ${env.BUILD_URL}console

— Jenkins"""
        }

        always {
            // cleanup container
            sh "docker rm -f $CONTAINER_NAME || true"
        }
    }
}
