from swml import Answer, Hangup, SignalWireML
import unittest


class TestSignalWireML(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_answer_method(self):
        main_section = self.response.add_section('main')
        main_section.answer(max_duration=60)

        expected_swml = '{"sections": {"main": [{"answer": {"max_duration": 60}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_answer_instance(self):
        main_section = self.response.add_section('main')
        main_section_answer = Answer(max_duration=60)
        main_section.add_instruction(main_section_answer)

        expected_swml = '{"sections": {"main": [{"answer": {"max_duration": 60}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_hangup_method(self):
        main_section = self.response.add_section('main')
        main_section.hangup(reason='busy')

        expected_swml = '{"sections": {"main": [{"hangup": {"reason": "busy"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_hangup_instance(self):
        main_section = self.response.add_section('main')
        main_section_hangup = Hangup(reason='busy')
        main_section.add_instruction(main_section_hangup)

        expected_swml = '{"sections": {"main": [{"hangup": {"reason": "busy"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
