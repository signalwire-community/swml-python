from swml import Cond, SignalWireML
import unittest

class TestSWMLCond(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_cond_method(self):
        main_section = self.response.add_section('main')
        main_section.cond(when="var1 == 'value1'", then=["action1"], else_=["action2"])
        expected_swml = '{"sections": {"main": [{"cond": {"when": "var1 == \'value1\'", "then": ["action1"], "else": ["action2"]}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_cond_instance(self):
        main_section = self.response.add_section('main')
        cond_instruction = Cond(when="var1 == 'value1'", then=["action1"], else_=["action2"])
        main_section.add_instruction(cond_instruction)
        expected_swml = '{"sections": {"main": [{"cond": {"when": "var1 == \'value1\'", "then": ["action1"], "else": ["action2"]}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
