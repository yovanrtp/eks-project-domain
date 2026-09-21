pipeline {
    agent any
    stages {
        stage('Prepare Tools') {
            steps {
                sh '''
                    set -eux
                    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                    chmod +x kubectl
                    mv kubectl /usr/local/bin/
                '''
            }
        }
        stage('Deploy to K8s') {
            steps {
                sh '''
                    kubectl apply -f k8s/sample-deployment.yaml
                '''
            }
        }
    }
}