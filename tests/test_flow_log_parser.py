import unittest
import os
from generate_input_files import generator
from flow_log_parser import load_lookup_table, process_flow_log, write_output_files

class TestFlowLogParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        generator.main()
        cls.lookup_table_file = 'input/lookup_table.csv'
        cls.flow_log_file = 'input/flow_log.txt'
        cls.output_dir = 'output'
        if not os.path.exists(cls.output_dir):
            os.makedirs(cls.output_dir)

    def test_load_lookup_table(self):
        lookup_dict = load_lookup_table(self.lookup_table_file)
        self.assertTrue(isinstance(lookup_dict, dict))
        self.assertGreater(len(lookup_dict), 0)

    def test_process_flow_log(self):
        lookup_dict = load_lookup_table(self.lookup_table_file)
        tag_counts, port_protocol_counts = process_flow_log(self.flow_log_file, lookup_dict)
        self.assertTrue(isinstance(tag_counts, dict))
        self.assertTrue(isinstance(port_protocol_counts, dict))
        self.assertGreater(len(tag_counts), 0)
        self.assertGreater(len(port_protocol_counts), 0)

    def test_write_output_files(self):
        lookup_dict = load_lookup_table(self.lookup_table_file)
        tag_counts, port_protocol_counts = process_flow_log(self.flow_log_file, lookup_dict)
        write_output_files(tag_counts, port_protocol_counts, self.output_dir)

        tag_counts_file = os.path.join(self.output_dir, 'tag_counts.txt')
        port_protocol_counts_file = os.path.join(self.output_dir, 'port_protocol_count.txt')

        self.assertTrue(os.path.exists(tag_counts_file))
        self.assertTrue(os.path.exists(port_protocol_counts_file))

        with open(tag_counts_file, 'r') as file:
            contents = file.read()
            self.assertIn('Tag Counts:', contents)

        with open(port_protocol_counts_file, 'r') as file:
            contents = file.read()
            self.assertIn('Port/Protocol Combination Counts:', contents)

    def test_end_to_end(self):
        lookup_dict = load_lookup_table(self.lookup_table_file)
        tag_counts, port_protocol_counts = process_flow_log(self.flow_log_file, lookup_dict)
        write_output_files(tag_counts, port_protocol_counts, self.output_dir)

        tag_counts_file = os.path.join(self.output_dir, 'tag_counts.txt')
        port_protocol_counts_file = os.path.join(self.output_dir, 'port_protocol_count.txt')

        self.assertTrue(os.path.exists(tag_counts_file))
        self.assertTrue(os.path.exists(port_protocol_counts_file))

        # Basic checks on content
        with open(tag_counts_file, 'r') as file:
            contents = file.read()
            self.assertIn('untagged', contents)  # Check for presence of any tag or "untagged" label
            self.assertIn('Tag', contents)  # Ensure the header is present

        with open(port_protocol_counts_file, 'r') as file:
            contents = file.read()
            self.assertIn('tcp', contents)  # Check for presence of a protocol
            self.assertIn('Port', contents)  # Ensure the header is present

    @classmethod
    def tearDownClass(cls):
        # Cleanup the generated files after tests
        files_to_remove = [
            cls.lookup_table_file,
            cls.flow_log_file,
            os.path.join(cls.output_dir, 'tag_counts.txt'),
            os.path.join(cls.output_dir, 'port_protocol_count.txt')
        ]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)
        if os.path.exists(cls.output_dir):
            os.rmdir(cls.output_dir)

if __name__ == '__main__':
    unittest.main()
