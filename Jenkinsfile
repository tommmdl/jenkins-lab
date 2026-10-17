pipeline {
    agent any
    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 5, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    parameters {
        booleanParam(name: 'SIMULATE_FAILURE', defaultValue: false,
                     description: 'Exercise the failure path / Exercitar falha')
    }
    stages {
        stage('Validate') {
            steps {
                sh 'bash -n scripts/build.sh'
            }
        }
        stage('Build report') {
            steps {
                sh 'bash scripts/build.sh'
            }
        }
        stage('Failure drill') {
            when { expression { params.SIMULATE_FAILURE } }
            steps {
                error('Intentional failure drill / Falha intencional')
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'artifacts/report.txt', allowEmptyArchive: true
        }
        cleanup {
            deleteDir()
        }
    }
}
