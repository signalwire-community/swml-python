import unittest
from swml import SignalWireML, SipRefer

class TestSipRefer(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_sip_refer_with_instance(self):
        main_section = self.response.add_section('main')
        # Create a SipRefer instance with a more complex result parameter
        sip_refer_instance = SipRefer("sip:alice@example.com", {"when": "vars.return_value != 'success'",
                                                                "then": {"goto": {"label": "refer", "max": 2}}})
        main_section.add_instruction(sip_refer_instance)

        expected_swml = '{"sections": {"main": [{"sip_refer": {"to_uri": "sip:alice@example.com", "result": {"when": "vars.return_value != \'success\'", "then": {"goto": {"label": "refer", "max": 2}}}}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_sip_refer_with_method(self):
        main_section = self.response.add_section('main')
        # Call the sip_refer method with a more complex result parameter
        main_section.sip_refer(to_uri="sip:alice@example.com",
                               result={"when": "vars.return_value != 'success'",
                                       "then": {"goto": {"label": "refer", "max": 2}}})

        expected_swml = '{"sections": {"main": [{"sip_refer": {"to_uri": "sip:alice@example.com", "result": {"when": "vars.return_value != \'success\'", "then": {"goto": {"label": "refer", "max": 2}}}}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)