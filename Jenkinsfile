pipeline {
    agent any
    environment {
        NEXUS_URL = 'http://nexus-service.devops.svc.cluster.local:8081'
        REGISTRY = 'nexus-service.devops.svc.cluster.local:8081'
        IMAGE_NAME = 'sample-webapp'
        IMAGE_TAG = 'latest'
        SONARQUBE_URL = 'http://sonarqube-service.devops.svc.cluster.local:9000'
    }
    stages {
        stage('Prepare Tools') {
            steps {
                sh '''
                    set -eux
                    apt-get update
                    apt-get install -y python3 python3-pip python3-venv docker.io curl unzip
                    export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
                    export PATH=$JAVA_HOME/bin:$PATH
                '''
            }
        }
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
        /*stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_AUTH_TOKEN')]) {
                    sh '''
                        if [ ! -x sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner ]; then
                            curl -sSLo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
                            unzip sonar-scanner.zip
                        fi
                        ./sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner \
                          -Dsonar.projectKey=sample-webapp \
                          -Dsonar.sources=. \
                          -Dsonar.host.url=$SONARQUBE_URL \
                          -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }
        */
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