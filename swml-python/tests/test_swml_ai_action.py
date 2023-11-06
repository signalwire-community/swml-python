import json
import unittest
from swml import *


class TestAIIntegration(unittest.TestCase):

    def setUp(self):
        # This will be our base SignalWireML object for testing
        self.response = SignalWireML()

    def test_ai_with_datamap_and_actions(self):
        # Create an AI instance with necessary parameters including DataMap and actions
        prompt_params = PromptParams(text="How can I assist you?")
        ai_params = AIParams(direction="bidirectional", wait_for_user=True)

        # Actions
        say_action = Say(message="Weather forecast received.")
        context_switch_action = ContextSwitch(system_prompt="Switching context")
        stop_action = Stop()
        toggle_functions_action = ToggleFunctions(active=True, functions=["function1", "function2"])
        back_to_back_functions_action = BackToBackFunctions(back_to_back_functions=True)
        set_meta_data_action = SetMetaData(meta_data={"key": "value"})
        playback_bg_action = PlaybackBG(file="background_music.mp3", wait=True)
        stop_playback_bg_action = StopPlaybackBG(stop_playback=True)
        user_input_action = UserInput(input_text="User response")

        # DataMap Expression Output with all actions
        data_map_expression_output = DataMapExpressionOutput(
            response="Weather forecast received.",
            action=[
                say_action,
                context_switch_action,
                stop_action,
                toggle_functions_action,
                back_to_back_functions_action,
                set_meta_data_action,
                playback_bg_action,
                stop_playback_bg_action,
                user_input_action
            ]
        )

        data_map_expression = DataMap.Expressions(
            string="rain",
            pattern="It's going to rain",
            output=data_map_expression_output
        )

        data_map = DataMap(expressions=[data_map_expression])

        # Create the SWAIGFunction and SWAIGParams
        function_property_detail = SWAIGFunction.FunctionArgs.PropertyDetail(
            type_="string",
            description="Location for weather lookup"
        )

        function_arg = SWAIGFunction.FunctionArgs(
            type_="object",
            properties={"location": function_property_detail}
        )

        swaig_function = SWAIGFunction(
            function="get_weather",
            purpose="Get the weather",
            argument=function_arg,
            data_map=data_map
        )

        swaig_params = AI.SWAIGParams(functions=[swaig_function])

        # Add AI to a Section
        main_section = self.response.add_section('main')
        main_section.ai(prompt=prompt_params, params=ai_params, SWAIG=swaig_params)

        # Generate the SWML to verify the output
        generated_swml = self.response.generate_swml()

        # Note: Update this expected SWML to match the actual expected output including all new actions.
        expected_swml = json.dumps({"sections": {"main": [{"ai": {"prompt": {"text": "How can I assist you?"}, "params": {"direction": "bidirectional", "wait_for_user": True}, "SWAIG": {"functions": [{"function": "get_weather", "purpose": "Get the weather", "argument": {"type": "object", "properties": {"location": {"type": "string", "description": "Location for weather lookup"}}}, "data_map": {"expressions": [{"string": "rain", "pattern": "It's going to rain", "output": {"response": "Weather forecast received.", "action": [{"say": "Weather forecast received."}, {"context_switch": {"system_prompt": "Switching context"}}, {"stop": True}, {"toggle_functions": {"active": True, "functions": ["function1", "function2"]}}, {"back_to_back_functions": True}, {"set_meta_data": {"meta_data": {"key": "value"}}}, {"playback_bg": {"file": "background_music.mp3", "wait": True}}, {"stop_playback": True}, {"input_text": "User response"}]}}]}}]}}}]}})

        self.assertEqual(generated_swml, expected_swml)


if __name__ == '__main__':
    unittest.main()
