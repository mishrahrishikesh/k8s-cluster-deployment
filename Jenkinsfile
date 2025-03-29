pipeline{
    agent any
    parameters{
        string(name: 'WORKER_COUNTER', defaultValue: '2', description: 'Number of worker nodes')
        string(name: 'WorkerIP', description: 'Write comma seprated Worker IPs')
        choice(name: 'ACTION', choices:['Deploy', 'Destroy', 'Test'])
    }
    stages{
        stage('Update Inventory'){
            def ips = params.WorkerIP.split(',')
            steps{
                script{
                    sh """python3 generate_inventory.py 1 ${params.WORKER_COUNTER} 10.129.155.220 ${ips.each {ip -> ${ip}}}"""
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