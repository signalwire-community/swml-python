import unittest

from swml import SignalWireML
from swml.SWMLTypes import Answer


class TestSignalWireML(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_add_instruction_with_Instruction_instance(self):
        main_section = self.response.add_section('main')

        main_section.add_instruction(Answer())

        expected_swml = '{"sections": {"main": ["answer"]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_empty_instructions(self):
        main_section = self.response.add_section('main')

        try:
            main_section.add_instruction()

        except TypeError:
            pass

        try:
            main_section.add_instruction({})

        except ValueError:
            pass

        expected_swml = '{"sections": {"main": [{}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_dict(self):
        main_section = self.response.add_section('main')

        main_section.add_instruction({"answer": {}})

        expected_swml = '{"sections": {"main": [{"answer": {}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
