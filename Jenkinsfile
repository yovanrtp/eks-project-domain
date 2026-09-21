pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
    - cat
    tty: true
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker
  - name: python
    image: python:3.12-slim
    command:
    - cat
    tty: true
  volumes:
  - name: docker-config
    secret:
      secretName: regcred
"""
            defaultContainer 'python'
        }
    }
    environment {
        REGISTRY = 'nexus-service.devops.svc.cluster.local:8081'
        IMAGE_NAME = 'sample-webapp'
        IMAGE_TAG = 'latest'
    }
    stages {
        stage('Test')
 {
            steps {
                container('python') {
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
        }
        stage('Kaniko Build & Push') {
            steps {
                container('kaniko') {
                    sh '''
                        /kaniko/executor \
                          --dockerfile=Dockerfile \
                          --context=/home/jenkins/agent/workspace/$JOB_NAME \
                          --destination=$REGISTRY/$IMAGE_NAME:$IMAGE_TAG
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
            sh 'true'
            deleteDir()
        }
    }
}