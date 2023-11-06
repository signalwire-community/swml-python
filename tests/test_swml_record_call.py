from swml import SignalWireML, RecordCall
import unittest

class TestSWMLRecordCall(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_record_call_method(self):
        main_section = self.response.add_section('main')
        main_section.record_call(
            control_id="12345",
            stereo=True,
            format_="mp3",
            direction="both",
            terminators="#",
            beep=True,
            input_sensitivity=0.5,
            initial_timeout=5.0,
            end_silence_timeout=3.0
        )

        expected_swml = '{"sections": {"main": [{"record_call": {"control_id": "12345", "stereo": true, "format": "mp3", "direction": "both", "terminators": "#", "beep": true, "input_sensitivity": 0.5, "initial_timeout": 5.0, "end_silence_timeout": 3.0}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_record_call_instance(self):
        main_section = self.response.add_section('main')
        main_section_record_call = RecordCall(
            control_id="12345",
            stereo=True,
            format_="mp3",
            direction="both",
            terminators="#",
            beep=True,
            input_sensitivity=0.5,
            initial_timeout=5.0,
            end_silence_timeout=3.0
        )
        main_section.add_instruction(main_section_record_call)
        expected_swml = '{"sections": {"main": [{"record_call": {"control_id": "12345", "stereo": true, "format": "mp3", "direction": "both", "terminators": "#", "beep": true, "input_sensitivity": 0.5, "initial_timeout": 5.0, "end_silence_timeout": 3.0}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

