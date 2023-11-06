import unittest
from swml import SignalWireML, Denoise


class TestDenoise(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_denoise_with_instance(self):
        main_section = self.response.add_section('main')
        main_section.add_instruction(Denoise())

        expected_swml = '{"sections": {"main": ["denoise"]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_denoise_with_method(self):
        main_section = self.response.add_section('main')
        main_section.denoise()

        expected_swml = '{"sections": {"main": ["denoise"]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
