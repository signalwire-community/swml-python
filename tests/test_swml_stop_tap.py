import unittest
from swml import SignalWireML, StopTap

class TestSWMLStopTap(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_stop_tap_method(self):
        main_section = self.response.add_section('main')
        main_section.stop_tap(control_id="123")
        expected_swml = '{"sections": {"main": [{"stop_tap": {"control_id": "123"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_stop_tap_instance(self):
        main_section = self.response.add_section('main')
        main_section_stop_tap = StopTap(control_id="123")
        main_section.add_instruction(main_section_stop_tap)
        expected_swml = '{"sections": {"main": [{"stop_tap": {"control_id": "123"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)