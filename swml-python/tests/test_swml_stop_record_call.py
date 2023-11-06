from swml import StopRecordCall, SignalWireML
import unittest


class TestSWMLStopRecordCall(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_stop_record_call_method(self):
        main_section = self.response.add_section('main')
        main_section.stop_record_call(control_id="12345")

        expected_swml = '{"sections": {"main": [{"stop_record_call": {"control_id": "12345"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_stop_record_call_instance(self):
        main_section = self.response.add_section('main')
        main_section_stop_record_call = StopRecordCall(control_id="12345")
        main_section.add_instruction(main_section_stop_record_call)

        expected_swml = '{"sections": {"main": [{"stop_record_call": {"control_id": "12345"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
