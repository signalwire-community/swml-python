import unittest
from swml import SignalWireML, Return

class TestSWMLReturn(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_return_method(self):
        main_section = self.response.add_section('main')
        main_section.return_(return_value="value1")
        expected_swml = '{"sections": {"main": [{"return": {"return_value": "value1"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_return_instance(self):
        main_section = self.response.add_section('main')
        return_instruction = Return(return_value="value1")
        main_section.add_instruction(return_instruction)
        expected_swml = '{"sections": {"main": [{"return": {"return_value": "value1"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
