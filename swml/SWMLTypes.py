import json
from typing import Union, Dict, Any, Optional, List, Tuple


class Instruction:
    def __init__(self, class_name: str = None, **kwargs):
        self.name = class_name
        self.params = {k: v for k, v in kwargs.items() if v is not None and k != 'class_name'}

    def serialize(self):
        def serialize_recursively(obj):

            if isinstance(obj, Instruction):
                return obj.serialize()
            elif isinstance(obj, dict):
                return {k: serialize_recursively(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize_recursively(item) for item in obj]
            else:
                return obj

        serialized_params = serialize_recursively(self.params)

        if self.name:
            if not serialized_params:
                return self.name  # Return name only if there are no parameters
            return {self.name: serialized_params}
        else:
            return serialized_params  # Return only the serialized parameters if no name is provided


class Action(Instruction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SWMLAction(Action):
    def __init__(self, swml: Union[Dict[str, Any], str]):
        if isinstance(swml, dict):
            swml = json.dumps(swml)
        if not isinstance(swml, str):
            raise ValueError("SWML object must be a string or a dictionary.")

        super().__init__(SWML=swml)


class ContextSwitch(Action):
    def __init__(self, system_prompt: str, user_prompt: str = None, consolidate: bool = None):
        super().__init__(
            class_name='context_switch',
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            consolidate=consolidate
        )


class Say(Action):
    def __init__(self, message: str):
        super().__init__(say=message)


class Stop(Action):
    def __init__(self, stop: bool = True):
        super().__init__(stop=stop)


class ToggleFunctions(Action):
    def __init__(self, active: bool = True, functions: Union[List[str], str] = None):
        super().__init__(
            class_name='toggle_functions',
            active=active,
            functions=functions
        )


class BackToBackFunctions(Action):
    def __init__(self, back_to_back_functions: bool = False):
        super().__init__(
            back_to_back_functions=back_to_back_functions
        )


class SetMetaData(Action):
    def __init__(self, meta_data: Dict[str, Any]):
        super().__init__(
            class_name='set_meta_data',
            meta_data=meta_data
        )


class PlaybackBG(Action):
    def __init__(self, file: str, wait: bool = False):
        super().__init__(
            class_name='playback_bg',
            file=file,
            wait=wait
        )


class StopPlaybackBG(Action):
    def __init__(self, stop_playback: bool = True):
        super().__init__(
            stop_playback=stop_playback
        )


class UserInput(Action):
    def __init__(self, input_text: str):
        super().__init__(
            input_text=input_text
        )


# LanguageParams Class
class LanguageParams(Instruction):

    def __init__(self,
                 name: Optional[str] = None,
                 code: Optional[str] = None,
                 voice: Optional[str] = None,
                 fillers: Optional[List[str]] = None,
                 engine: Optional[str] = None):
        super().__init__(name=name, code=code, voice=voice, fillers=fillers, engine=engine)


class Pronounce(Instruction):
    def __init__(self, replace: Optional[str] = None, with_: Optional[str] = None, ignore_case: Optional[bool] = None):
        params = {'replace': replace, 'with': with_, 'ignore_case': ignore_case}

        super().__init__(**params)


# PromptParams Class
class PromptParams(Instruction):
    def __init__(self,
                 text: Optional[str] = None,
                 language: Optional[str] = None,
                 temperature: Optional[float] = None,
                 top_p: Optional[float] = None,
                 confidence: Optional[float] = None,
                 presence_penalty: Optional[float] = None,
                 frequency_penalty: Optional[float] = None,
                 result: Optional[Union[Dict[str, Any], List[Any]]] = None):
        super().__init__(
            text=text,
            language=language,
            temperature=temperature,
            top_p=top_p,
            confidence=confidence,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            result=result
        )


class DataMapExpressionOutput(Instruction):
    def __init__(self, response: Optional[str] = None,
                 action: Union[Optional[List], Dict[str, Any]] = None):
        super().__init__(
            response=response,
            action=action
        )


# DataMapExpression Class
class DataMapExpression(Instruction):
    DataMapExpressionOutput = DataMapExpressionOutput

    def __init__(self, string: str, pattern: str, output: Union[DataMapExpressionOutput, Dict[str, Any]]):
        super().__init__(
            string=string,
            pattern=pattern,
            output=output
        )


class DataMapWebhookOutput(Instruction):
    def __init__(self, response: Optional[str] = None,
                 action: Union[Optional[List], Dict[str, Any]] = None):
        super().__init__(
            response=response,
            action=action
        )


# DataMapWebhook Class
class DataMapWebhook(Instruction):
    DataMapWebhookOutput = DataMapWebhookOutput

    def __init__(self, url: str, headers: Dict[str, str], method: str,
                 output: Union[DataMapWebhookOutput, Dict[str, Any]]):
        super().__init__(
            url=url,
            headers=headers,
            method=method,
            output=output
        )


# DataMap Class
class DataMap(Instruction):
    Expressions = DataMapExpression
    Webhooks = DataMapWebhook

    def __init__(self, expressions: Union[Optional[List[DataMapExpression]], Optional[List]] = None,
                 webhooks: Union[Optional[List[DataMapWebhook]], Optional[List]] = None):
        super().__init__(
            expressions=expressions,
            webhooks=webhooks
        )


# SWAIGFunction Class
class SWAIGFunction(Instruction):
    DataMap = DataMap

    class FunctionArgs(Instruction):
        class PropertyDetail(Instruction):
            def __init__(self,
                         type_: Optional[str] = None,
                         description: Optional[str] = None):
                params = {'type': type_, 'description': description}
                super().__init__(**params)

        def __init__(self,
                     type_: str,
                     properties: Optional[Dict[str, PropertyDetail]] = None):
            params = {'type': type_, 'properties': properties}
            super().__init__(**params)

    def __init__(self,
                 function: str,
                 purpose: str,
                 active: Optional[bool] = None,
                 web_hook_url: Optional[str] = None,
                 web_hook_auth_user: Optional[str] = None,
                 web_hook_auth_pass: Optional[str] = None,
                 argument: Union[Optional[Dict[str, Any]], Optional[FunctionArgs]] = None,
                 data_map: Union[Optional[Dict[str, Any]], Optional[DataMap]] = None):
        super().__init__(
            function=function,
            purpose=purpose,
            active=active,
            web_hook_url=web_hook_url,
            web_hook_auth_user=web_hook_auth_user,
            web_hook_auth_pass=web_hook_auth_pass,
            argument=argument,
            data_map=data_map
        )


# SWAIGDefaults Class
class SWAIGDefaults(Instruction):
    def __init__(self,
                 web_hook_url: Optional[str] = None,
                 web_hook_auth_user: Optional[str] = None,
                 web_hook_auth_password: Optional[str] = None,
                 meta_data: Optional[Dict[str, Any]] = None,
                 meta_data_token: Optional[str] = None):
        super().__init__(
            web_hook_url=web_hook_url,
            web_hook_auth_user=web_hook_auth_user,
            web_hook_auth_password=web_hook_auth_password,
            meta_data=meta_data,
            meta_data_token=meta_data_token
        )


# SWAIGParams Class
class SWAIGParams(Instruction):
    def __init__(self,
                 functions: Optional[Union[List[SWAIGFunction], List[Dict[str, Any]]]] = None,
                 defaults: Optional[Union[SWAIGDefaults, Dict[str, Any]]] = None,
                 includes: Optional[List[Dict[str, Any]]] = None):
        super().__init__(
            functions=functions,
            defaults=defaults,
            includes=includes
        )


# AIParams Class
class AIParams(Instruction):
    def __init__(self,
                 direction: Optional[str] = None,
                 wait_for_user: Optional[bool] = None,
                 end_of_speech_timeout: Optional[int] = None,
                 attention_timeout: Optional[int] = None,
                 inactivity_timeout: Optional[int] = None,
                 background_file: Optional[str] = None,
                 background_file_loops: Optional[int] = None,
                 background_file_volume: Optional[int] = None,
                 ai_volume: Optional[int] = None,
                 local_tz: Optional[str] = None,
                 conscience: Optional[bool] = None,
                 save_conversation: Optional[bool] = None,
                 conversation_id: Optional[str] = None,
                 digit_timeout: Optional[int] = None,
                 digit_terminators: Optional[str] = None,
                 energy_level: Optional[int] = None,
                 swaig_allow_swml: Optional[bool] = None):
        super().__init__(
            direction=direction,
            wait_for_user=wait_for_user,
            end_of_speech_timeout=end_of_speech_timeout,
            attention_timeout=attention_timeout,
            inactivity_timeout=inactivity_timeout,
            background_file=background_file,
            background_file_loops=background_file_loops,
            background_file_volume=background_file_volume,
            ai_volume=ai_volume,
            local_tz=local_tz,
            conscience=conscience,
            save_conversation=save_conversation,
            conversation_id=conversation_id,
            digit_timeout=digit_timeout,
            digit_terminators=digit_terminators,
            energy_level=energy_level,
            swaig_allow_swml=swaig_allow_swml
        )


# AI Class
class AI(Instruction):
    PromptParams = PromptParams
    SWAIGFunction = SWAIGFunction
    SWAIGParams = SWAIGParams
    SWAIGDefaults = SWAIGDefaults
    AIParams = AIParams
    LanguageParams = LanguageParams
    Pronounce = Pronounce

    def __init__(self,
                 voice: Optional[str] = None,
                 prompt: Optional[Union[Dict[str, Any], PromptParams]] = None,
                 post_prompt: Optional[Dict[str, Any]] = None,
                 post_prompt_url: Optional[str] = None,
                 post_prompt_auth_user: Optional[str] = None,
                 post_prompt_auth_password: Optional[str] = None,
                 params: Optional[Union[Dict[str, Any], AIParams]] = None,
                 SWAIG: Optional[Union[Dict[str, Any], SWAIGParams]] = None,
                 hints: Optional[List[str]] = None,
                 languages: Optional[List[Dict[str, Any]]] = None,
                 pronounce: Union[Optional[Dict[str, Any]], Pronounce] = None):
        super().__init__("ai", voice=voice, prompt=prompt, post_prompt=post_prompt, post_prompt_url=post_prompt_url,
                         post_prompt_auth_user=post_prompt_auth_user,
                         post_prompt_auth_password=post_prompt_auth_password,
                         params=params, SWAIG=SWAIG, hints=hints,
                         languages=languages, pronounce=pronounce)


class Answer(Instruction):
    def __init__(self, max_duration: Optional[int] = None):
        super().__init__(class_name='answer', max_duration=max_duration)


class Connect(Instruction):
    def __init__(self, from_number: Optional[str] = None, headers: Optional[Dict[str, str]] = None,
                 codecs: Optional[str] = None, webrtc_media: Optional[bool] = None,
                 session_timeout: Optional[int] = None, ringback: Optional[List[str]] = None,
                 timeout: Optional[int] = None, max_duration: Optional[int] = None,
                 answer_on_bridge: Optional[bool] = None, call_state_url: Optional[str] = None,
                 call_state_events: Optional[List[str]] = None, result: Optional[Union[Dict, List]] = None,
                 serial_parallel: Optional[List[List[Dict[str, str]]]] = None,
                 serial: Optional[List[Dict[str, str]]] = None, parallel: Optional[List[Dict[str, str]]] = None,
                 to_number: Optional[str] = None):
        dialing_params = [serial_parallel, serial, parallel, to_number]
        if sum(param is not None for param in dialing_params) != 1:
            raise ValueError(
                "Exactly one of the dialing parameters (serial_parallel, serial, parallel, to_number) must be provided.")
        super().__init__(class_name='connect',
                         from_number=from_number,
                         headers=headers,
                         codecs=codecs,
                         webrtc_media=webrtc_media,
                         session_timeout=session_timeout,
                         ringback=ringback,
                         timeout=timeout,
                         max_duration=max_duration,
                         answer_on_bridge=answer_on_bridge,
                         call_state_url=call_state_url,
                         call_state_events=call_state_events,
                         result=result,
                         serial_parallel=serial_parallel,
                         serial=serial,
                         parallel=parallel,
                         to_number=to_number
                         )


class Cond(Instruction):
    def __init__(self, when: str, then: Union[Instruction], else_: Union[Instruction]):
        params = {'when': when, 'then': then, 'else': else_}

        super().__init__(class_name='cond', **params)


class Denoise(Instruction):
    def __init__(self):
        super().__init__(class_name='denoise')


class Execute(Instruction):
    def __init__(self, dest: str, params: Optional[Dict[str, Any]] = None):
        super().__init__(class_name='execute', dest=dest, params=params)


class Hangup(Instruction):
    def __init__(self, reason=None):
        if reason is not None and reason not in ['busy', 'hangup', 'decline']:
            raise ValueError("Hangup reason must be one of the following: 'hangup', 'busy', or 'decline'")
        super().__init__(class_name='hangup', reason=reason)


class JoinRoom(Instruction):
    def __init__(self, name: str):
        super().__init__(class_name='join_room', name=name)


class Play(Instruction):
    def __init__(self,
                 urls: Optional[List[str]] = None,
                 url: Optional[str] = None,
                 volume: Optional[float] = None,
                 say_voice: Optional[str] = None,
                 silence: Optional[float] = None,
                 ring: Optional[Tuple[float, str]] = None):
        if url is not None and urls is not None:
            raise ValueError("Cannot provide both 'url' and 'urls'. Please provide only one.")

        super().__init__(class_name='play', urls=urls, url=url, volume=volume, say_voice=say_voice, silence=silence,
                         ring=ring)


class Prompt(Instruction):
    def __init__(self,
                 play: Union[str, List[str]],
                 volume: Optional[float] = None,
                 say_voice: Optional[str] = None,
                 say_language: Optional[str] = None,
                 say_gender: Optional[str] = None,
                 max_digits: Optional[int] = None,
                 terminators: Optional[str] = None,
                 digit_timeout: Optional[float] = None,
                 initial_timeout: Optional[float] = None,
                 speech_timeout: Optional[float] = None,
                 speech_end_timeout: Optional[float] = None,
                 speech_language: Optional[str] = None,
                 speech_hints: Optional[List[str]] = None,
                 result: Optional[Union[dict, list]] = None):
        super().__init__(
            class_name='prompt',
            play=play,
            volume=volume,
            say_voice=say_voice,
            say_language=say_language,
            say_gender=say_gender,
            max_digits=max_digits,
            terminators=terminators,
            digit_timeout=digit_timeout,
            initial_timeout=initial_timeout,
            speech_timeout=speech_timeout,
            speech_end_timeout=speech_end_timeout,
            speech_language=speech_language,
            speech_hints=speech_hints,
            result=result
        )


class ReceiveFax(Instruction):

    def __init__(self):
        super().__init__(class_name='receive_fax')


class Record(Instruction):
    def __init__(self,
                 stereo: Optional[bool] = None,
                 format_: Optional[str] = None,
                 direction: Optional[str] = None,
                 terminators: Optional[str] = None,
                 beep: Optional[bool] = None,
                 input_sensitivity: Optional[float] = None,
                 initial_timeout: Optional[float] = None,
                 end_silence_timeout: Optional[float] = None):
        if format_ is not None and format_ not in ['wav', 'mp3']:
            raise ValueError("Format must be one of the following: 'wav', 'mp3'")
        if direction is not None and direction not in ['speak', 'listen', 'both']:
            raise ValueError("Direction must be one of the following: 'speak', 'listen', 'both'")

        super().__init__(
            stereo=stereo,
            format=format_,
            direction=direction,
            terminators=terminators,
            beep=beep,
            input_sensitivity=input_sensitivity,
            initial_timeout=initial_timeout,
            end_silence_timeout=end_silence_timeout
        )


class RecordCall(Instruction):
    def __init__(self,
                 control_id: Optional[str] = None,
                 stereo: Optional[bool] = None,
                 format_: Optional[str] = None,
                 direction: Optional[str] = None,
                 terminators: Optional[str] = None,
                 beep: Optional[bool] = None,
                 input_sensitivity: Optional[float] = None,
                 initial_timeout: Optional[float] = None,
                 end_silence_timeout: Optional[float] = None):
        if format_ is not None and format_ not in ['wav', 'mp3']:
            raise ValueError("Format must be one of the following: 'wav', 'mp3'")
        if direction is not None and direction not in ['speak', 'listen', 'both']:
            raise ValueError("Direction must be one of the following: 'speak', 'listen', 'both'")
        super().__init__(
            class_name='record_call',
            control_id=control_id,
            stereo=stereo,
            format=format_,
            direction=direction,
            terminators=terminators,
            beep=beep,
            input_sensitivity=input_sensitivity,
            initial_timeout=initial_timeout,
            end_silence_timeout=end_silence_timeout
        )


class Request(Instruction):
    def __init__(self,
                 url: str,
                 method: str,
                 headers: Optional[Dict[str, str]] = None,
                 body: Optional[Union[str, Dict[str, Any]]] = None,
                 timeout: Optional[float] = None,
                 connect_timeout: Optional[float] = None,
                 save_variables: Optional[bool] = None):
        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
            raise ValueError(
                "Invalid request method. Method must be one of the following: 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'")

        super().__init__(
            class_name='request',
            url=url,
            method=method,
            headers=headers,
            body=body,
            timeout=timeout,
            connect_timeout=connect_timeout,
            save_variables=save_variables
        )


class Return(Instruction):
    def __init__(self, return_value: Optional[Any] = None):
        super().__init__(class_name='return', return_value=return_value)


class SendDigits(Instruction):
    def __init__(self, digits: str):
        super().__init__(class_name='send_digits', digits=digits)


class SendFax(Instruction):
    def __init__(self, document: str, header_info: Optional[str] = None, identity: Optional[str] = None):
        super().__init__(class_name='send_fax', document=document, header_info=header_info, identity=identity)


class SendSMS(Instruction):
    def __init__(self,
                 to_number: str,
                 from_number: str,
                 body: str,
                 media: Optional[List[str]] = None,
                 region: Optional[str] = None,
                 tags: Optional[List[str]] = None):
        super().__init__(class_name="send_sms", to_number=to_number, from_number=from_number, body=body, media=media,
                         region=region, tags=tags)


class Set(Instruction):
    def __init__(self, variables: Dict[str, Any]):
        super().__init__(class_name="set", variables=variables)


class SipRefer(Instruction):
    def __init__(self,
                 to_uri: str,
                 result: Optional[Union[dict, list]]):
        super().__init__(class_name="sip_refer", to_uri=to_uri, result=result)


class StopDenoise(Instruction):
    def __init__(self):
        super().__init__(class_name="stop_denoise")


class StopRecordCall(Instruction):
    def __init__(self,
                 control_id: Optional[str] = None):
        super().__init__(class_name="stop_record_call", control_id=control_id)


class StopTap(Instruction):
    def __init__(self,
                 control_id: str):
        super().__init__(class_name="stop_tap", control_id=control_id)


class Switch(Instruction):
    def __init__(self,
                 variable: str,
                 case: Optional[Dict[str, list]] = None,
                 default: Optional[List[Any]] = None):
        super().__init__(class_name="switch", variable=variable, case=case, default=default)


class Tap(Instruction):
    def __init__(self,
                 uri: str,
                 control_id: Optional[str] = None,
                 direction: Optional[str] = None,
                 codec: Optional[str] = None,
                 rtp_ptime: Optional[int] = None):
        valid_directions = ["speak", "hear", "both"]
        valid_codecs = ["PCMU", "PCMA"]
        if direction and direction not in valid_directions:
            raise ValueError(f"Invalid direction. Expected one of {valid_directions}")
        if codec and codec not in valid_codecs:
            raise ValueError(f"Invalid codec. Expected one of {valid_codecs}")
        super().__init__(class_name="tap", uri=uri, control_id=control_id, direction=direction, codec=codec,
                         rtp_ptime=rtp_ptime)


class Transfer(Instruction):
    def __init__(self,
                 dest: str,
                 params: Optional[Dict[str, Any]] = None,
                 meta: Optional[Dict[str, Any]] = None,
                 result: Optional[Union[dict, list]] = None):
        super().__init__(class_name="transfer", dest=dest, params=params, meta=meta, result=result)


class Unset(Instruction):
    def __init__(self, vars_: Union[str, List[str]]):
        super().__init__(class_name="unset", vars=vars_)
