import sys
no_of_master=int(sys.argv[1])
no_of_worker=int(sys.argv[2])
master_ips=[]
worker_ips=[]

start=3
total_ips=no_of_master+no_of_worker

for ip in range(start,start+no_of_master):
    master_ips.append(sys.argv[ip])
  
for ip in range(start+no_of_master,start+total_ips):
    worker_ips.append(sys.argv[ip])
    
count=1

with open('inventory.yml', 'w') as file:
    file.write(f'all:\n')
    file.write(f' children:\n')
    file.write(f'  master:\n')
    file.write(f'    hosts:\n')
for ip in master_ips:
    with open('inventory.yml', 'a') as file:
        file.write(f'     master{count}:\n')
        file.write(f'      ansible_host: {ip}\n')
        count+=1
count=1
with open('inventory.yml', 'a') as file:
    file.write(f'  worker:\n')
    file.write(f'    hosts:\n')

for ip in worker_ips:
    with open('inventory.yml', 'a') as file:
        file.write(f'     worker{count}:\n')
        file.write(f'       ansible_host: {ip}\n')
        count+=1
with open('inventory.yml', 'a') as file:
    file.write(f' vars:')
    file.write('''
    ansible_become: true
    ansible_become_method: su
    ansible_become_password: RvShos
    ansible_become_user: root
    ansible_password: password
    ansible_python_interpreter: /usr/bin/python3
    ansible_ssh_extra_args: -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null
    ansible_user: pmgradmin 
               ''')