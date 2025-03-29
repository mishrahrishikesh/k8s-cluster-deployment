pipeline{
    agent any
    parameters{
        string(name: 'MasterNodes', defaultValue: '2', description: 'Number of Worker nodes')
        string(name: 'WorkerNodes', defaultValue: '2', description: 'Number of Master nodes')
        text(name: 'MasterIP', description: 'Write space seprated Master IPs')
        text(name: 'WorkerIP', description: 'Write space seprated Worker IPs')
        choice(name: 'ACTION', choices:['Deploy', 'Destroy', 'Test'])
    }
    stages{
        stage('Update Inventory'){
            steps{
                script{
                    def no_of_ip=params.MasterIP.split(' ').size()
                    echo "${no_of_ip}"
                    echo "${params.MasterNodes}"
                    if(params.MasterNodes == no_of_ip){
                        sh """python3 generate_inventory.py 1 ${params.WorkerNodes} ${MasterIP} ${WorkerIP}"""
                    }
                    else{
                        sh 'echo NotCorrect'
                    }
                }
            }
        }
        stage('Build'){
            steps{
                script{
                    if(params.ACTION == 'Deploy'){
                        sh 'ansible-playbook -i inventory.yml k8s_deployment.yml'
                    }
                    if(params.ACTION == 'Destroy'){
                        sh 'ansible-playbook -i inventory.yml k8s_destroy.yml'
                    }
                    else{
                        sh 'hostname'
                    }
                }
            }
        }
    }
}