import unittest
from swml import SignalWireML, Tap

class TestSWMLTap(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_tap_method(self):
        main_section = self.response.add_section('main')
        main_section.tap(uri="sip:test@domain.com", control_id="123", direction="both", codec="PCMU", rtp_ptime=20)
        expected_swml = '{"sections": {"main": [{"tap": {"uri": "sip:test@domain.com", "control_id": "123", "direction": "both", "codec": "PCMU", "rtp_ptime": 20}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_tap_instance(self):
        main_section = self.response.add_section('main')
        main_section_tap = Tap(uri="sip:test@domain.com", control_id="123", direction="both", codec="PCMU", rtp_ptime=20)
        main_section.add_instruction(main_section_tap)
        expected_swml = '{"sections": {"main": [{"tap": {"uri": "sip:test@domain.com", "control_id": "123", "direction": "both", "codec": "PCMU", "rtp_ptime": 20}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)