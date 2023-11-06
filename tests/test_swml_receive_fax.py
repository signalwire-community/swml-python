import unittest
from swml import SignalWireML, ReceiveFax

class TestReceiveFax(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_receive_fax_with_instance(self):
        main_section = self.response.add_section('main')
        main_section.add_instruction(ReceiveFax())

        expected_swml = '{"sections": {"main": ["receive_fax"]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_receive_fax_with_method(self):
        main_section = self.response.add_section('main')
        main_section.receive_fax()

        expected_swml = '{"sections": {"main": ["receive_fax"]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)