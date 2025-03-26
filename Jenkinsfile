pipeline {
    agent any
    parameters {
        // Number of master and worker nodes
        int(name: 'MASTER_COUNTER', defaultValue: 1, description: 'Number of master nodes')
        int(name: 'WORKER_COUNTER', defaultValue: 2, description: 'Number of worker nodes')

        // IP addresses for master and worker nodes
        string(name: 'Master_IPs', defaultValue: '', description: 'Comma-separated list of master node IPs')
        string(name: 'Worker_IPs', defaultValue: '', description: 'Comma-separated list of worker node IPs')

        // Action choice: Deploy or Destroy
        choice(name: 'ACTION', choices: ['Deploy', 'Destroy'], description: 'Choose whether to Deploy or Destroy the Kubernetes cluster')
    }
    stages {
        stage('Validate Inputs') {
            steps {
                script {
                    // Split the input IPs into lists
                    def masterIPs = params.Master_IPs.split(',').collect { it.trim() }
                    def workerIPs = params.Worker_IPs.split(',').collect { it.trim() }

                    // Validate the number of IPs matches the number of nodes
                    if (masterIPs.size() != params.MASTER_COUNTER) {
                        error "The number of master nodes (${params.MASTER_COUNTER}) does not match the number of master IPs (${masterIPs.size()})"
                    }

                    if (workerIPs.size() != params.WORKER_COUNTER) {
                        error "The number of worker nodes (${params.WORKER_COUNTER}) does not match the number of worker IPs (${workerIPs.size()})"
                    }

                    echo "Input validation passed."
                }
            }
        }

        stage('Update Inventory') {
            steps {
                script {
                    // Split the input IPs into lists and pass them to the Python script
                    def masterIPs = params.Master_IPs.split(',').collect { it.trim() }
                    def workerIPs = params.Worker_IPs.split(',').collect { it.trim() }

                    // Call the Python script to generate the inventory based on the user inputs
                    sh "python3 generate_inventory.py ${params.MASTER_COUNTER} ${params.WORKER_COUNTER} ${masterIPs.join(' ')} ${workerIPs.join(' ')}"
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    // Depending on the ACTION parameter, either deploy or destroy
                    if (params.ACTION == 'Deploy') {
                        sh 'ansible-playbook -i inventory.yml k8s_deployment.yml'
                    } else {
                        sh 'ansible-playbook -i inventory.yml k8s_destroy.yml'
                    }
                }
            }
        }
    }
}
