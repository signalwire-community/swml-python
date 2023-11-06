import unittest
from swml import SignalWireML, SendSMS

class TestSWMLSendSMS(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_send_sms_method(self):
        main_section = self.response.add_section('main')
        main_section.send_sms(to_number="+1XXXXXXXXXX", from_number="+1XXXXXXXXXX", body="Message Body", media=["url1", "url2"], region="us", tags=["Custom", "data"])
        expected_swml = '{"sections": {"main": [{"send_sms": {"to_number": "+1XXXXXXXXXX", "from_number": "+1XXXXXXXXXX", "body": "Message Body", "media": ["url1", "url2"], "region": "us", "tags": ["Custom", "data"]}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_send_sms_instance(self):
        send_sms_instance = SendSMS(to_number="+1XXXXXXXXXX", from_number="+1XXXXXXXXXX", body="Message Body", media=["url1", "url2"], region="us", tags=["Custom", "data"])
        main_section = self.response.add_section('main')
        main_section.add_instruction(send_sms_instance)
        expected_swml = '{"sections": {"main": [{"send_sms": {"to_number": "+1XXXXXXXXXX", "from_number": "+1XXXXXXXXXX", "body": "Message Body", "media": ["url1", "url2"], "region": "us", "tags": ["Custom", "data"]}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)