from swml import SignalWireML, Play
import unittest

class TestSWMLPlay(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_play_method(self):
        main_section = self.response.add_section('main')
        main_section.play(
            urls="http://example.com/audio.mp3",
            volume=0.5,
            say_voice="en-US",
            silence=5.0,
            ring=(5.0, "us")
        )

        expected_swml = '{"sections": {"main": [{"play": {"urls": "http://example.com/audio.mp3", "volume": 0.5, "say_voice": "en-US", "silence": 5.0, "ring": [5.0, "us"]}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_play_instance(self):
        main_section = self.response.add_section('main')
        main_section_play = Play(
            urls="http://example.com/audio.mp3",
            volume=0.5,
            say_voice="en-US",
            silence=5.0,
            ring=(5.0, "us")
        )
        main_section.add_instruction(main_section_play)

        expected_swml = '{"sections": {"main": [{"play": {"urls": "http://example.com/audio.mp3", "volume": 0.5, "say_voice": "en-US", "silence": 5.0, "ring": [5.0, "us"]}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
