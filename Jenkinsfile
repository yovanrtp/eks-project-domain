pipeline {
    agent any
    stages {
        stage('Deploy to K8s') {
            steps {
                sh '''
                    kubectl apply -f k8s/sample-deployment.yaml
                '''
            }
        }
    }
}