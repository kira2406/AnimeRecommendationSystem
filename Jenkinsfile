pipeline{
    agent any

    environment {
        VENV_DIR = "venv"
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
    }
}