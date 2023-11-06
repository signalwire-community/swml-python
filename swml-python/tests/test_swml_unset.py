import unittest
from swml import SignalWireML, Unset

class TestSWMLUnset(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_unset_method(self):
        main_section = self.response.add_section('main')
        main_section.unset(_vars="var1")
        expected_swml = '{"sections": {"main": [{"unset": {"vars": "var1"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_unset_instance(self):
        main_section = self.response.add_section('main')
        unset_instruction = Unset(vars_="var1")
        main_section.add_instruction(unset_instruction)
        expected_swml = '{"sections": {"main": [{"unset": {"vars": "var1"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
