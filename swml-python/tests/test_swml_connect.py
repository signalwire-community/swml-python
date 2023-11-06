import unittest
from swml import SignalWireML, Connect


class TestSWMLConnect(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_connect_method(self):
        main_section = self.response.add_section('main')
        main_section.connect(from_number="+1XXXXXXXXXX", headers={"X-Custom-Header": "value"}, codecs="PCMU",
                             webrtc_media=True, session_timeout=180, ringback=["http://example.com/ringback.mp3"],
                             timeout=60, max_duration=7200, answer_on_bridge=True,
                             call_state_url="http://example.com/call_state",
                             call_state_events=["created", "ringing", "answered", "ended"],
                             result={"case": {"connected": [{"hangup": {}}],
                                              "default": [{"execute": "voicemail"}, {"hangup": {}}]}},
                             to_number="+1XXXXXXXXXX")
        expected_swml = '{"sections": {"main": [{"connect": {"from_number": "+1XXXXXXXXXX", "headers": {"X-Custom-Header": "value"}, "codecs": "PCMU", "webrtc_media": true, "session_timeout": 180, "ringback": ["http://example.com/ringback.mp3"], "timeout": 60, "max_duration": 7200, "answer_on_bridge": true, "call_state_url": "http://example.com/call_state", "call_state_events": ["created", "ringing", "answered", "ended"], "result": {"case": {"connected": [{"hangup": {}}], "default": [{"execute": "voicemail"}, {"hangup": {}}]}}, "to_number": "+1XXXXXXXXXX"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_connect_instance(self):
        connect_instance = Connect(from_number="+1XXXXXXXXXX", headers={"X-Custom-Header": "value"}, codecs="PCMU",
                                   webrtc_media=True, session_timeout=180, ringback=["http://example.com/ringback.mp3"],
                                   timeout=60, max_duration=7200, answer_on_bridge=True,
                                   call_state_url="http://example.com/call_state",
                                   call_state_events=["created", "ringing", "answered", "ended"],
                                   result={"case": {"connected": [{"hangup": {}}],
                                                    "default": [{"execute": "voicemail"}, {"hangup": {}}]}},
                                   serial=[{"to_number": "+1XXXXXXXXXX"}, {"to_number": "+1XXXXXXXXXX"}])
        main_section = self.response.add_section('main')
        main_section.add_instruction(connect_instance)
        expected_swml = '{"sections": {"main": [{"connect": {"from_number": "+1XXXXXXXXXX", "headers": {"X-Custom-Header": "value"}, "codecs": "PCMU", "webrtc_media": true, "session_timeout": 180, "ringback": ["http://example.com/ringback.mp3"], "timeout": 60, "max_duration": 7200, "answer_on_bridge": true, "call_state_url": "http://example.com/call_state", "call_state_events": ["created", "ringing", "answered", "ended"], "result": {"case": {"connected": [{"hangup": {}}], "default": [{"execute": "voicemail"}, {"hangup": {}}]}}, "serial": [{"to_number": "+1XXXXXXXXXX"}, {"to_number": "+1XXXXXXXXXX"}]}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
