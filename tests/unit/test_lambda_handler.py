from lambdas.process.app import handler


def test_handler_returns_ok():
    result = handler({"message": "hello"}, None)

    assert result == {
        "status": "ok",
        "received": {"message": "hello"},
    }


def test_handler_preserves_input():
    event = {
        "user_id": 123,
        "action": "process",
    }

    result = handler(event, None)

    assert result["received"] == event


def test_handler_handles_empty_input():
    result = handler({}, None)

    assert result == {
        "status": "ok",
        "received": {},
    }