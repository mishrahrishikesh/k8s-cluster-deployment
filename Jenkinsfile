pipeline{
    agent any
    parameters{
        choice(name: 'ACTION', choices:['Deploy', 'Destroy'])
    }
    stages{
        stage('Build'){
            steps{
                script{
                    if(params.ACTION == 'Deploy'){
                        sh 'ansible-playbook -i host k8s_deployment.yml'
                    }
                    else{
                        sh 'ansible-playbook -i host k8s_destroy.yml'
                    }
                }
            }
        }
    }
}