pipeline {
    agent any
    parameters {
        string(name: 'MASTER_COUNTER', defaultValue: '1', description: 'Number of master nodes')
        string(name: 'WORKER_COUNTER', defaultValue: '2', description: 'Number of worker nodes')

        string(name: 'Master_IPs', defaultValue: '', description: 'Comma-separated list of master node IPs')
        string(name: 'Worker_IPs', defaultValue: '', description: 'Comma-separated list of worker node IPs')

        choice(name: 'ACTION', choices: ['Deploy', 'Destroy'], description: 'Choose whether to Deploy or Destroy the Kubernetes cluster')
    }
    stages {
        stage('Validate Inputs') {
            steps {
                script {
                    // Convert the counters from string to integer
                    def masterCount = params.MASTER_COUNTER.toInteger()
                    def workerCount = params.WORKER_COUNTER.toInteger()

                    // Split the input IPs into lists
                    def masterIPs = params.Master_IPs.split(',').collect { it.trim() }
                    def workerIPs = params.Worker_IPs.split(',').collect { it.trim() }

                    // Validate the number of IPs matches the number of nodes
                    if (masterIPs.size() != masterCount) {
                        error "The number of master nodes (${masterCount}) does not match the number of master IPs (${masterIPs.size()})"
                    }

                    if (workerIPs.size() != workerCount) {
                        error "The number of worker nodes (${workerCount}) does not match the number of worker IPs (${workerIPs.size()})"
                    }

                    echo "Input validation passed."
                }
            }
        }

        stage('Update Inventory') {
            steps {
                script {
                    // Convert the counters from string to integer
                    def masterCount = params.MASTER_COUNTER.toInteger()
                    def workerCount = params.WORKER_COUNTER.toInteger()

                    // Split the input IPs into lists and pass them to the Python script
                    def masterIPs = params.Master_IPs.split(',').collect { it.trim() }
                    def workerIPs = params.Worker_IPs.split(',').collect { it.trim() }

                    // Call the Python script to generate the inventory based on the user inputs
                    sh "python3 generate_inventory.py ${masterCount} ${workerCount} ${masterIPs.join(' ')} ${workerIPs.join(' ')}"
                }
            }
        }

        // New stage for checking node connectivity with normal ping
        stage('Check Node Connectivity') {
            steps {
                script {
                    // Convert the counters from string to integer
                    def masterCount = params.MASTER_COUNTER.toInteger()
                    def workerCount = params.WORKER_COUNTER.toInteger()

                    // Split the input IPs into lists
                    def masterIPs = params.Master_IPs.split(',').collect { it.trim() }
                    def workerIPs = params.Worker_IPs.split(',').collect { it.trim() }

                    // Combine all IPs into one list
                    def allIPs = masterIPs + workerIPs

                    // Check connectivity using the normal ping command
                    allIPs.each { ip ->
                        try {
                            echo "Pinging node ${ip}..."
                            // Run the normal ping command (check for 1 packet)
                            def result = sh(script: "ping -c 1 -w 5 ${ip}", returnStatus: true)
                            if (result != 0) {
                                error "Failed to connect to ${ip}. Aborting!"
                            } else {
                                echo "Successfully connected to ${ip}"
                            }
                        } catch (Exception e) {
                            error "Error while pinging ${ip}. Aborting!"
                        }
                    }
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
