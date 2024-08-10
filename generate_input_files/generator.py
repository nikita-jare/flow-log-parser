import random
import csv
import os

# Get the project's root directory
project_root = os.path.dirname(os.path.dirname(__file__))

# Generate lookup_table.csv with up to 10,000 mappings
lookup_table_filename = os.path.join(project_root, 'input/lookup_table.csv')
lookup_tags = ['sv_P1', 'sv_P2', 'sv_P3', 'sv_P4', 'sv_P5']
protocols = ['tcp', 'udp', 'icmp']
ports = list(range(1, 65536))  # TCP/UDP ports range

# Function to generate the lookup table
def generate_lookup_table():
    lookup_data = []
    for _ in range(10000):
        port = random.choice(ports)
        protocol = random.choice(protocols)
        tag = random.choice(lookup_tags)
        lookup_data.append([port, protocol, tag])
    
    with open(lookup_table_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["dstport", "protocol", "tag"])
        writer.writerows(lookup_data)

# Function to generate the flow log
def generate_flow_log():
    flow_log_filename = os.path.join(project_root, 'input/flow_log.txt')
    log_entries = []

    # Create log entries
    for _ in range(150000):
        version = random.randint(2, 4)
        account_id = random.randint(100000000000, 999999999999)
        interface_id = f'eni-{random.randint(10000000, 99999999)}'
        src_addr = f'{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
        dst_addr = f'{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
        src_port = random.randint(1, 65535)
        dst_port = random.choice(ports)
        protocol = random.choice(protocols)
        packets = random.randint(1, 1000)
        bytes_ = packets * random.randint(40, 1500)
        start = random.randint(1, 10000000)
        end = start + random.randint(1, 10000)
        action = random.choice(['ACCEPT', 'REJECT'])
        log_status = random.choice(['OK', 'NODATA', 'SKIPDATA'])

        log_entry = f"{version} {account_id} {interface_id} {src_addr} {dst_addr} {src_port} {dst_port} {protocol} {packets} {bytes_} {start} {end} {action} {log_status}"
        log_entries.append(log_entry)

    with open(flow_log_filename, 'w') as file:
        file.write("\n".join(log_entries))

def main():
    input_dir = os.path.dirname(lookup_table_filename)
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    
    generate_lookup_table()
    generate_flow_log()

if __name__ == '__main__':
    main()