import csv
import logging
from collections import defaultdict
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Function to load the lookup table into a dictionary
def load_lookup_table(filename):
    lookup_dict = {}
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                key = (row['dstport'], row['protocol'].lower())
                lookup_dict[key] = row['tag'].lower()
        logging.info(f"Loaded lookup table from {filename}")
    except Exception as e:
        logging.error(f"Error loading lookup table: {e}")
        raise
    return lookup_dict

# Function to process the flow log and map to tags
def process_flow_log(flow_log_file, lookup_dict):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    protocol_map = {'6': 'tcp', '17': 'udp', '1': 'icmp'}
    try:
        with open(flow_log_file, 'r') as file:
            for line in file:
                fields = line.split()
                dstport = fields[6]  
                protocol = protocol_map.get(fields[7], fields[7]) 
                
                key = (dstport, protocol)
                tag = lookup_dict.get(key, "untagged")
                
                tag_counts[tag] += 1
                port_protocol_counts[key] += 1
            
        logging.info(f"Processed flow log from {flow_log_file}")
    except Exception as e:
        logging.error(f"Error processing flow log: {e}")
        raise
    
    return tag_counts, port_protocol_counts

# Function to write the counts to output files
def write_output_files(tag_counts, port_protocol_counts, output_dir='output'):
    try:
        with open(f'{output_dir}/tag_counts.txt', 'w') as file:
            file.write("Tag Counts:\n")
            file.write(f"{'Tag':<15} {'Count':<5}\n")
            for tag, count in tag_counts.items():
                file.write(f"{tag:<15} {count:<5}\n")
        
        with open(f'{output_dir}/port_protocol_count.txt', 'w') as file:
            file.write("Port/Protocol Combination Counts:\n\n")
            file.write(f"{'Port':<10} {'Protocol':<10} {'Count':<5}\n")
            for (port, protocol), count in port_protocol_counts.items():
                file.write(f"{port:<10} {protocol:<10} {count:<5}\n")
        
        logging.info(f"Output files written to {output_dir}")
    except Exception as e:
        logging.error(f"Error writing output files: {e}")
        raise

# Main function to run the program
def main():
    try:
        lookup_table_file = 'input/lookup_table.csv'
        flow_log_file = 'input/flow_log.txt'
        output_dir = 'output'

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        lookup_dict = load_lookup_table(lookup_table_file)
        tag_counts, port_protocol_counts = process_flow_log(flow_log_file, lookup_dict)
        write_output_files(tag_counts, port_protocol_counts, output_dir)
    
    except Exception as e:
        logging.critical(f"Program terminated due to an error: {e}")

if __name__ == '__main__':
    main()