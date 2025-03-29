pipeline{
    agent any
    parameters{
        string(name: 'MasterNodes', defaultValue: '1', description: 'Number of Worker nodes')
        string(name: 'WorkerNodes', defaultValue: '2', description: 'Number of Master nodes')
        text(name: 'MasterIP', description: 'Write space seprated Master IPs')
        text(name: 'WorkerIP', description: 'Write space seprated Worker IPs')
        choice(name: 'ACTION', choices:['Deploy', 'Destroy', 'Test'])
    }
    stages{
        stage('Update Inventory'){
            steps{
                script{
                    def no_of_master_ip=params.MasterIP.split(' ').size()
                    def no_of_master_nodes=params.MasterNodes.toInteger()
                    def no_of_worker_ip=params.WorkerIP.split(' ').size()
                    def no_of_worker_nodes=params.WorkerNodes.toInteger()
                    if( no_of_master_nodes == no_of_master_ip && no_of_worker_nodes == no_of_worker_ip ){
                        sh """python3 generate_inventory.py ${params.MasterNodes} ${params.WorkerNodes} ${MasterIP} ${WorkerIP}"""
                    }
                    else{
                       echo "Number of IPs not matching number of nodes"
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