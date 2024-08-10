# Flow Log Parser

## Overview

This program processes a flow log file and assigns tags to each log entry based on a lookup table. It then generates an output file with the count of matches for each tag and the count of matches for each port/protocol combination.

## Files

- `lookup_table.csv`: Contains the port, protocol, and tag mappings.
- `flow_log.txt`: Contains the flow log data to be processed.
- `output/`: Directory where the output file will be saved.
- `output/tag_counts.txt`: Output file with the count of matches for each tag.
- `output/protocol_counts.txt`: Output file with the count of matches for each port/protocol combination.

## Assumptions

- The log entries in the flow log file are formatted similarly to AWS VPC flow logs.
- The program is case-insensitive when matching protocols and tags.
- Entries that do not match any port/protocol combination in the lookup table are considered "Untagged".

## How to Run

1. Ensure the input files (`lookup_table.csv` and `flow_log.txt`) are present in the `input/` directory. You can generate them using the `generate_input_files/generator.py` script and check the `input/` directory for the results.

Command: `python generate_input_files/generator.py`

2. Run the program to process the flow log and generate the output.

Command: `python flow_log_parser.py`

3. Check the `output/` directory for the results.

## Testing

- Run the test script in the `tests/` directory.

Command: `python -m unittest tests/test_flow_log_parser.py`

- The output and input directory are cleared after tests are run. You can comment out the `tearDownClass` method in the `tests/test_flow_log_parser.py` file to keep the files in directory.
