import pytest

headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
}


@pytest.fixture(autouse=True)
def mock_settings_env_vars(monkeypatch):
    global app
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    from src import app


def test_respond_error():
    value = app.respond("Error message")
    assert value == {
        "statusCode": 400,
        "body": '"Error message"',
        "headers": headers,
    }


def test_respond_ok():
    value = app.respond(None, "OK message")
    assert value == {
        "statusCode": 200,
        "body": '"OK message"',
        "headers": headers,
    }


def test_api_health():
    event = {"resource": "/health", "httpMethod": "GET"}
    val = app.lambda_handler(event, None)
    assert val == {
        "statusCode": 200,
        "body": '{"status": "OK"}',
        "headers": headers,
    }


def test_api_increment_get(mocker):
    mocker.patch("src.app.get_counter_value", return_value={"counter_value": "20"})
    event = {"resource": "/increment", "httpMethod": "GET"}
    val = app.lambda_handler(event, None)
    assert val == {
        "statusCode": 200,
        "body": '{"counter_value": "20"}',
        "headers": headers,
    }


def test_api_increment_post(mocker):
    mocker.patch("src.app.increment_counter", return_value="OK")
    event = {"resource": "/increment", "httpMethod": "POST"}
    val = app.lambda_handler(event, None)
    assert val == {
        "statusCode": 200,
        "body": '"OK"',
        "headers": headers,
    }
