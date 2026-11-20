from types import SimpleNamespace
import sys

from app import ask


class FakeChat:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)
        return next(self.responses)


def _response(text, input_tokens, output_tokens):
    return SimpleNamespace(
        usage_metadata=SimpleNamespace(
            prompt_token_count=input_tokens,
            candidates_token_count=output_tokens,
        ),
        text=text,
    )


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    chat = FakeChat([_response("回答", 12, 7)])

    class FakeChats:
        def create(self, **kwargs):
            return chat

    class FakeClient:
        def __init__(self, **kwargs):
            self.chats = FakeChats()

    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")

    assert ask.ask("質問") == "回答"
    assert capsys.readouterr().out.strip() == "[tokens] input=12 output=7"


def test_main_reuses_chat_for_follow_up_questions(monkeypatch, capsys):
    chat = FakeChat([_response("回答1", 12, 7), _response("回答2", 20, 9)])

    class FakeChats:
        def create(self, **kwargs):
            return chat

    class FakeClient:
        def __init__(self, **kwargs):
            self.chats = FakeChats()

    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(sys, "argv", ["app.ask", "最初の質問"])
    input_values = iter(["", "続けての質問", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_values))

    ask.main()

    assert chat.messages == ["最初の質問", "続けての質問"]
    assert "[tokens] input=12 output=7" in capsys.readouterr().out