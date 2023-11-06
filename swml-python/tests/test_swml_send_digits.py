import unittest
from swml import SignalWireML, SendDigits

class TestSWMLSendDigits(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_send_digits_method(self):
        main_section = self.response.add_section('main')
        main_section.send_digits(digits="012345")
        expected_swml = '{"sections": {"main": [{"send_digits": {"digits": "012345"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_send_digits_instance(self):
        send_digits_instance = SendDigits("012345")
        main_section = self.response.add_section('main')
        main_section.add_instruction(send_digits_instance)
        expected_swml = '{"sections": {"main": [{"send_digits": {"digits": "012345"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

