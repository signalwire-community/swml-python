import unittest
from swml import SignalWireML, StopDenoise

class TestStopDenoise(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_stop_denoise_with_instance(self):
        main_section = self.response.add_section('main')
        main_section.add_instruction(StopDenoise())

        expected_swml = '{"sections": {"main": ["stop_denoise"]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_stop_denoise_with_method(self):
        main_section = self.response.add_section('main')
        main_section.stop_denoise()

        expected_swml = '{"sections": {"main": ["stop_denoise"]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)