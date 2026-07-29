import json
import datetime
from openai._types import NOT_GIVEN
from constants import full_config
from helpers import get_system_message


class BaseLLM:
    def __init__(self, client, config={}, data={}) -> None:
        self.openai = client
        self.config = config if not config == {} else full_config
        self.data = data

    def chat_completion(self, messages=[], **kwargs):
        response_format = self.config.get(
            "response_format", kwargs.get("response_format"))
        if not response_format or response_format == "":
            response_format = NOT_GIVEN
        try:
            dicto = dict(
                model=self.config.get("model", NOT_GIVEN),
                temperature=self.config.get("temperature", 0),
                top_p=self.config.get("top_p", 0.95),
                presence_penalty=self.config.get("presence_penalty", 0),
                frequency_penalty=self.config.get("frequency_penalty", 0),
                response_format=response_format,
                stream=self.config.get("stream", False),
                messages=self.messages if messages == [] else messages,
            )
            completion = self.openai.chat.completions.create(**dicto)
        except Exception as e:
            print("chat completion", e)
        else:
            if self.config.get("stream"):
                response = ""
                reasoning = ""
                thinking = False
                for chunk in completion:
                    if chunk:
                        if not chunk.choices[0].finish_reason:
                            reason = None
                            if hasattr(chunk.choices[0].delta, "reasoning"):
                                reason = chunk.choices[0].delta.reasoning
                            if reason is not None:
                                if not thinking:
                                    thinking = True
                                    print("Thinking:\n")
                                print(reason, end="", flush=True)
                                reasoning += reason
                            token = chunk.choices[0].delta.content
                            if token != '':
                                if thinking:
                                    thinking = False
                                    print("\n\nResponse:\n")
                                    # yield "\n\nResponse:\n"
                                print(token, end="", flush=True)
                                response += token
                print()

                return response.strip()

            else:
                if "refusal" in completion.choices[0].message:
                    print("Refused!")
                    print(completion.choices[0].message.refusal)
                return completion.choices[0].message.content


class LLMUtils:

    def save(self, name):
        with open(f"./chapters/{name}.json", 'w') as f:
            json.dump(self.messages, f)
        return "Conversation saved."

    def load(self, name):
        with open(f"./chapters/{name}.json", 'r') as f:
            self.messages = json.loads(f.read())
        return "Conversation loaded."

    def ct(self, value):
        self.config['temperature'] = float(value)
        return self.config

    def ctp(self, value):
        self.config['top_p'] = float(value)
        return self.config

    def cpp(self, value):
        self.config['presence_penalty'] = float(value)
        return self.config

    def cfp(self, value):
        self.config['frequency_penalty'] = float(value)
        return self.config


class BasicLLM(BaseLLM, LLMUtils):

    def __init__(self, client, config={}, data={}) -> None:
        super().__init__(client, config, data)
        self.messages = self.data.get("messages", [])
        self.instructions_folder = "./personas/"
        self.data = data

    def reset(self, system_prompt=None):
        self.messages = self.data.get("messages", [])
        if system_prompt:
            self.append_message("system", system_prompt, unique=True)

    def append_message(self, role, content, name=None, unique=None):
        if not name and role == "assistant":
            name = self.config.get("name")

        if unique and name:
            self.messages.append(dict(role=role, name=name, content=content))

        elif len(self.messages) > 0 and self.messages[-1]['role'] == role:
            if name:
                self.messages.append(
                    dict(role=role, name=name, content=content))
                return

        self.messages.append(dict(role=role, content=content))

    def respond(self, **kwargs):
        response_format = kwargs.get("response_format", NOT_GIVEN)

        if response_format in globals():
            kwargs["response_format"] = globals()[response_format]

        response = self.generate(**kwargs).strip()

        self.append_message(
            role='assistant',
            content=response,
            name=self.config.get("name"))

        return response

    def responding(self, message=None, name=None, response_format=NOT_GIVEN):
        response = self.stream(
            message, name=name, response_format=response_format)
        self.append_message(role='assistant', content=response,
                            name=self.config.get("name"))
        return response

    def inject_variables(self, message, name):
        def get_ordinal_suffix(day: int) -> str:
            return {
                1: 'st', 2: 'nd', 3: 'rd'}.get(
                    day % 10, 'th') if day not in (
                        11, 12, 13) else 'th'
        kwargs = {}
        now = datetime.datetime.now()
        # kwargs["date_r"] = f"{
        #     now.strftime('%B')} {
        #         now.day}{
        #             get_ordinal_suffix(int(now.day))}, {
        #                 now.year} - {
        #                     now.hour: 02d}: {
        #                         (math.ceil(int(now.minute) / 15) * 15) % 60: 02d} - {
        #                             now.strftime('%A')}"

        kwargs["date"] = f"{
            now.strftime('%B')} {
                now.day}{
                    get_ordinal_suffix(int(now.day))}, {
                        now.year}"

        kwargs["date_t"] = f"{
            now.strftime('%B')} {
                now.day}{
                    get_ordinal_suffix(int(now.day))}, {
                        now.year} - {
                            now.hour % 12: 02d} {
                                'PM' if now.hour > 12 else 'AM'}, {
                                    now.strftime('%A')}"

        kwargs["date_p"] = f"{
            now.strftime('%B')} {
                now.day}{
                    get_ordinal_suffix(int(now.day))}, {
                        now.year} - {
                            now.hour: 02d}: {
                                now.minute: 02d}, {
                                    now.strftime('%A')}"

        kwargs["time"] = f"{
            now.hour % 12: 02d} {
                'PM' if now.hour > 12 else 'AM'}, {
                    now.strftime('%A')}"

        kwargs["time_p"] = f"{
            now.hour: 02d}: {
                now.minute: 02d}"

        self.config.update(kwargs)
        return message.format(**self.config)

    def refresh_system(self, rules=None, hijack=None, insert=False):
        if len(self.messages) > 1 and self.messages[0]["role"] == "system":
            self.messages = self.messages[1:]

        system_message = self.config.get("system_message")

        if system_message == "" or system_message is None:
            system_message = get_system_message(self.config.get("name"))

        for msg in self.messages:
            msg["content"] = self.inject_variables(
                msg['content'], self.config.get('name'))

        if system_message is not None:
            system_message = self.inject_variables(
                system_message, self.config.get("name"))

        if system_message and not system_message == "":
            self.messages.insert(
                0, dict(role="system", content=system_message))

    def align_messages(self):
        self.messages = [
            msg for msg in self.messages
            if ("content" in msg and msg['content'] != "")]

        if len(self.messages) > 1 and self.messages[0]["role"] == "system":
            while self.messages[1]["role"] == "assistant":
                self.messages.pop(1)

    def generate(self, message=None, name=None, **kwargs):
        if message:
            self.append_message("user", message, name)

        self.config.update(kwargs)
        self.refresh_system()

        messages = kwargs.get("messages")

        if messages or messages == []:
            messages.append(
                {
                    'role': 'user',
                    'content': [{'text': message, 'type': 'text'}],
                    'metadata': None,
                    'options': None,
                    'name': name
                }
            )
            return self.chat_completion(**kwargs)
        return self.chat_completion(self.messages, **kwargs)

    def change_model(self, model):
        self.config["model"] = model
        return f"Model changed to {model}."
