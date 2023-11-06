from swml import SignalWireML, JoinRoom
import unittest

class TestSWMLJoinRoom(unittest.TestCase):
    def setUp(self):
        self.response = SignalWireML()

    def test_join_room_method(self):
        main_section = self.response.add_section('main')
        main_section.join_room(name="Room1")

        expected_swml = '{"sections": {"main": [{"join_room": {"name": "Room1"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_join_room_instance(self):
        main_section = self.response.add_section('main')
        main_section_join_room = JoinRoom(name="Room1")
        main_section.add_instruction(main_section_join_room)

        expected_swml = '{"sections": {"main": [{"join_room": {"name": "Room1"}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
