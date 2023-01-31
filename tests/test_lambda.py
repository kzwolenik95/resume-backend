import pytest

headers = {"Content-Type": "application/json"}


@pytest.fixture(autouse=True)
def mock_settings_env_vars(monkeypatch):
    global my_backend_function
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    import my_backend_function


def test_respond_error():
    value = my_backend_function.respond("Error message")
    assert value == {
        "statusCode": 400,
        "body": '"Error message"',
        "headers": headers,
    }


def test_respond_ok():
    value = my_backend_function.respond(None, "OK message")
    assert value == {
        "statusCode": 200,
        "body": '"OK message"',
        "headers": headers,
    }

def test_api_health():
    event = {"resource": "/health", "httpMethod": "GET"}
    val = my_backend_function.lambda_handler(event)
    assert val == {
        "statusCode": 200,
        "body": '{"status": "OK"}',
        "headers": headers,
    }


def test_api_increment_get(mocker):
    mocker.patch(
        "my_backend_function.get_counter_value", return_value={"counter_value": "20"}
    )
    event = {"resource": "/increment", "httpMethod": "GET"}
    val = my_backend_function.lambda_handler(event)
    assert val == {
        "statusCode": 200,
        "body": '{"counter_value": "20"}',
        "headers": headers,
    }

def test_api_increment_post(mocker):
    mocker.patch(
        "my_backend_function.increment_counter", return_value="OK"
    )
    event = {"resource": "/increment", "httpMethod": "POST"}
    val = my_backend_function.lambda_handler(event)
    assert val == {
        "statusCode": 200,
        "body": '"OK"',
        "headers": headers,
    }