import sys
import yaml

def generate_inventory(master_count, worker_count, master_ips, worker_ips):
    # Initialize the inventory structure
    inventory = {
        'all': {
            'vars': {
                'ansible_user': 'pmgradmin',
                'ansible_password': 'password',
                'ansible_become': True,
                'ansible_become_method': 'su',
                'ansible_become_user': 'root',
                'ansible_become_password': 'RvShos',
                'ansible_python_interpreter': '/usr/bin/python3',
                'ansible_ssh_extra_args': "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
            },
            'children': {}
        }
    }

    # Generate master node section
    master_nodes = {}
    for i in range(1, master_count + 1):
        master_nodes[f"master{i}"] = {'ansible_host': master_ips[i-1]}

    inventory['all']['children']['master'] = {
        'hosts': master_nodes
    }

    # Generate worker node section
    worker_nodes = {}
    for i in range(1, worker_count + 1):
        worker_nodes[f"worker{i}"] = {'ansible_host': worker_ips[i-1]}

    inventory['all']['children']['worker'] = {
        'hosts': worker_nodes
    }

    # Save the generated inventory to a YAML file
    with open('inventory.yml', 'w') as file:
        yaml.dump(inventory, file)

    print("\nInventory has been successfully generated and saved to 'inventory.yml'.")

def main():
    # Check if the correct number of arguments are passed
    if len(sys.argv) < 3:
        print("Usage: python generate_inventory.py <num_masters> <num_workers> <master_ips...> <worker_ips...>")
        sys.exit(1)

    # Parse command line arguments
    master_count = int(sys.argv[1])
    worker_count = int(sys.argv[2])
    
    # Ensure that there are enough IPs provided
    if len(sys.argv[3:]) != master_count + worker_count:
        print(f"Error: {master_count + worker_count} IP addresses are required.")
        sys.exit(1)

    # Split the IP addresses into master and worker lists
    master_ips = sys.argv[3:3+master_count]
    worker_ips = sys.argv[3+master_count:3+master_count+worker_count]

    # Generate the inventory
    generate_inventory(master_count, worker_count, master_ips, worker_ips)

if __name__ == '__main__':
    main()
