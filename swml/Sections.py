from .SWMLTypes import *


class Section:
    def __init__(self, name: str):
        self.name = name
        self._actions = []

    def add_instruction(self, instruction):
        if isinstance(instruction, Instruction):
            serialized_instruction = instruction.serialize()
        elif isinstance(instruction, dict):
            # Handle dictionaries containing instructions
            serialized_instruction = {k: v.serialize() if isinstance(v, Instruction) else v for k, v in
                                      instruction.items()}
        else:
            raise TypeError("Invalid instruction type. Must be an instance of Instruction or dict.")
        self._actions.append(serialized_instruction)

    def ai(self, voice=None, prompt=None, post_prompt=None, post_prompt_url=None, post_prompt_auth_user=None,
           post_prompt_auth_password=None, params=None, SWAIG=None, hints=None, languages=None, pronounce=None):
        self.add_instruction(AI(voice, prompt, post_prompt, post_prompt_url, post_prompt_auth_user,
                                post_prompt_auth_password, params, SWAIG, hints, languages, pronounce))

    def answer(self, max_duration: Optional[int] = None):
        return self.add_instruction(Answer(max_duration=max_duration))

    def cond(self, when: str, then: Union[str, dict, Instruction], else_: Union[str, dict, Instruction]):
        return self.add_instruction(Cond(when=when, then=then, else_=else_))

    def connect(self, from_number=None, headers=None, codecs=None, webrtc_media=None, session_timeout=None,
                ringback=None, timeout=None, max_duration=None, answer_on_bridge=None, call_state_url=None,
                call_state_events=None, result=None, serial_parallel=None, serial=None, parallel=None, to_number=None):
        return self.add_instruction(
            Connect(from_number=from_number, headers=headers, codecs=codecs, webrtc_media=webrtc_media,
                    session_timeout=session_timeout, ringback=ringback, timeout=timeout, max_duration=max_duration,
                    answer_on_bridge=answer_on_bridge, call_state_url=call_state_url,
                    call_state_events=call_state_events, result=result, serial_parallel=serial_parallel,
                    serial=serial, parallel=parallel, to_number=to_number))

    def denoise(self):
        return self.add_instruction(Denoise())

    def execute(self, dest: str, params=None):
        return self.add_instruction(Execute(dest=dest, params=params))

    def hangup(self, reason=None):
        return self.add_instruction(Hangup(reason))

    def join_room(self, name: str):
        return self.add_instruction(JoinRoom(name))

    def play(self, url: Optional[str] = None, urls: Optional[List[str]] = None, volume: Optional[float] = None,
             say_voice: Optional[str] = None,
             silence: Optional[float] = None, ring: Optional[Tuple[float, str]] = None):
        return self.add_instruction(
            Play(url=url, urls=urls, volume=volume, say_voice=say_voice, silence=silence, ring=ring))

    def prompt(self, play, volume=None, say_voice=None, say_language=None, say_gender=None, max_digits=None,
               terminators=None, digit_timeout=None, initial_timeout=None, speech_timeout=None, speech_end_timeout=None,
               speech_language=None, speech_hints=None, result=None):
        self.add_instruction(Prompt(play, volume, say_voice, say_language, say_gender, max_digits, terminators,
                                    digit_timeout, initial_timeout, speech_timeout, speech_end_timeout, speech_language,
                                    speech_hints, result))

    def receive_fax(self):
        return self.add_instruction(ReceiveFax())

    def record(self, stereo=None, format_=None, direction=None, terminators=None, beep=None, input_sensitivity=None,
               initial_timeout=None, end_silence_timeout=None):
        self.add_instruction(Record(stereo, format_, direction, terminators, beep, input_sensitivity, initial_timeout,
                                    end_silence_timeout))

    def record_call(self, control_id=None, stereo=None, format_=None, direction=None, terminators=None, beep=None,
                    input_sensitivity=None, initial_timeout=None, end_silence_timeout=None):
        self.add_instruction(RecordCall(control_id, stereo, format_, direction, terminators, beep, input_sensitivity,
                                        initial_timeout, end_silence_timeout))

    def request(self, url, method, headers=None, body=None, timeout=None, connect_timeout=None, save_variables=False):
        self.add_instruction(Request(url, method, headers, body, timeout, connect_timeout, save_variables))

    def return_(self, return_value: Optional[Any] = None):
        self.add_instruction(Return(return_value))

    def send_digits(self, digits: str):
        self.add_instruction(SendDigits(digits))

    def send_fax(self, document: str, header_info: Optional[str] = None, identity: Optional[str] = None):
        self.add_instruction(SendFax(document=document, header_info=header_info, identity=identity))

    def send_sms(self, to_number, from_number, body, media=None, region=None, tags=None):
        self.add_instruction(SendSMS(to_number=to_number, from_number=from_number, body=body, media=media,
                                     region=region, tags=tags))

    def set(self, variables):
        self.add_instruction(Set(variables))

    def sip_refer(self, to_uri, result):
        self.add_instruction(SipRefer(to_uri, result))

    def stop_denoise(self):
        self.add_instruction(StopDenoise())

    def stop_record_call(self, control_id=None):
        self.add_instruction(StopRecordCall(control_id))

    def stop_tap(self, control_id):
        self.add_instruction(StopTap(control_id))

    def switch(self, variable, case=None, default=None):
        self.add_instruction(Switch(variable, case, default))

    def tap(self, uri, control_id=None, direction=None, codec=None, rtp_ptime=None):
        self.add_instruction(Tap(uri, control_id, direction, codec, rtp_ptime))

    def transfer(self, dest, params=None, meta=None, result=None):
        self.add_instruction(Transfer(dest, params, meta, result))

    def unset(self, _vars):
        self.add_instruction(Unset(_vars))
