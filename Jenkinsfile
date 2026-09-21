pipeline {
    agent any
    environment {
        NEXUS_URL = 'http://<NEXUS_HOST>:8081'
        NEXUS_REPO = 'docker-hosted'
        IMAGE_NAME = 'sample-webapp'
        IMAGE_TAG = 'latest'
        REGISTRY = '<NEXUS_HOST>:8082' // Nexus Docker repo port
    }
    stages {
        stage('Test') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    pip install pytest
                    pytest test_app.py
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $REGISTRY/$IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }
        stage('Push to Nexus') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'nexus-creds', usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')])
 {
                    sh '''
                        echo $NEXUS_PASS | docker login $REGISTRY -u $NEXUS_USER --password-stdin
                        docker push $REGISTRY/$IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }
        stage('Deploy to K8s') {
            steps {
                sh '''
                    sed "s|<NEXUS_REGISTRY>|$REGISTRY|g" k8s/deployment.yaml | kubectl apply -f -
                    kubectl apply -f k8s/service.yaml
                '''
            }
        }
    }
}