import unittest
from swml import SignalWireML, SendFax

class TestSendFax(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_send_fax_with_instance(self):
        main_section = self.response.add_section('main')
        main_section.add_instruction(SendFax(document="example.pdf", header_info="Header Info", identity="Identity"))

        expected_swml = '{"sections": {"main": [{"send_fax": {"document": "example.pdf", "header_info": "Header Info", "identity": "Identity"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_send_fax_with_method(self):
        main_section = self.response.add_section('main')
        main_section.send_fax(document="example.pdf", header_info="Header Info", identity="Identity")

        expected_swml = '{"sections": {"main": [{"send_fax": {"document": "example.pdf", "header_info": "Header Info", "identity": "Identity"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)