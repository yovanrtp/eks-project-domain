pipeline {
    agent any
    environment {
        REGISTRY = 'nexus-service.devops.svc.cluster.local:8081'
        IMAGE_NAME = 'sample-webapp'
        IMAGE_TAG = 'latest'
    }
    stages {
        stage('Test') {
            steps {
                sh '''
                    set -eux

                    python3 --version
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r requirements.txt
                    python3 -m pip install pytest
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
                withCredentials([usernamePassword(credentialsId: 'nexus-creds', usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                    sh '''
                        echo $NEXUS_PASS | docker login http://$REGISTRY -u $NEXUS_USER --password-stdin
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
    post {
        success {
            echo "BUILD COMPLETED SUCCESSFULLY"
        }
        failure {
            echo 'Build or deployment failed. Check the failed Jenkins stage and console output.'
        }
        always {
            sh 'docker image prune -f || true'
            deleteDir()
        }
    }
}