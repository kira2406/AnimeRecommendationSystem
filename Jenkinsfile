pipeline{
    agent any

    environment {
        VENV_DIR = "venv"
        GCP_PROJECT = 'eminent-yen-454107-u0'
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
        COMET_ML_APIKEY = credentials('COMET_ML_APIKEY')
    }

    stages{
        stage("Cloning from Github."){
            steps{
                script{
                    echo 'Cloning from Github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/kira2406/AnimeRecommendationSystem.git']])
                }
            }
        }

        stage("Set Up Environment") {
            steps {
                script {
                    echo "Creating .env file..."
                    sh """
                    echo "COMET_ML_APIKEY=${COMET_ML_APIKEY}" > .env
                    """
                }
            }
        }

        stage("Making a virtual env."){
            steps{
                script{
                    echo 'Making a virtual env'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc
                    '''
                    
                }
            }
        }

        stage("DVC Pull."){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'DVC Pull'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }
        stage("Build and push image to GCR."){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Build and push image to GCR'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/anime-rs:latest .
                        docker push gcr.io/${GCP_PROJECT}/anime-rs:latest
                        '''
                    }
                }
            }
        }
        stage("Deploying to Kubernetes"){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploying to Kubernetes'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials ml-project-app --region us-central1
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }
    }
}