import crybaby
from .conftest import TEST_SLACK_CHANNEL_ID, TEST_SLACK_TOKEN


def test_one_plus_one():
    assert 1 + 1 == 2


def test_setup(requests_mock):
    crybaby.setup(
        slack_token=TEST_SLACK_TOKEN, slack_channel_id=TEST_SLACK_CHANNEL_ID, check_joined_at_channel=True
    )
    assert requests_mock.call_count == 1
    try:
        raise Exception("Handled exception")
    except Exception as e:
        crybaby.catch(e)
    assert requests_mock.call_count == 2
    for history in requests_mock.request_history:
        if history.__str__() == "POST https://slack.com/api/chat.postMessage":
            assert history.json()["channel"] == TEST_SLACK_CHANNEL_ID
            assert "Handled exception" in history.json()["text"]


def test_setup_option_apply_code_block(requests_mock):
    crybaby.setup(
        slack_token=TEST_SLACK_TOKEN,
        slack_channel_id=TEST_SLACK_CHANNEL_ID,
        apply_code_block=False,
        check_joined_at_channel=True,
    )
    assert requests_mock.call_count == 1
    try:
        raise Exception("Handled exception")
    except Exception as e:
        crybaby.catch(e)
    assert requests_mock.call_count == 2
    for history in requests_mock.request_history:
        if history.__str__() == "POST https://slack.com/api/chat.postMessage":
            assert history.json()["channel"] == TEST_SLACK_CHANNEL_ID
            assert "Handled exception" in history.json()["text"]
            assert "```" not in history.json()["text"]


def test_setup_option_check_joined_at_channel(requests_mock):
    crybaby.setup(
        slack_token=TEST_SLACK_TOKEN,
        slack_channel_id=TEST_SLACK_CHANNEL_ID,
        check_joined_at_channel=True,
    )
    assert requests_mock.call_count == 1
    try:
        raise Exception("Handled exception")
    except Exception as e:
        crybaby.catch(e)
    assert requests_mock.call_count == 2
    for history in requests_mock.request_history:
        if history.__str__() == "POST https://slack.com/api/chat.postMessage":
            assert history.json()["channel"] == TEST_SLACK_CHANNEL_ID
            assert "Handled exception" in history.json()["text"]


def test_setup_option_check_joined_at_channel_defalut_false(requests_mock):
    crybaby.setup(
        slack_token=TEST_SLACK_TOKEN,
        slack_channel_id=TEST_SLACK_CHANNEL_ID,
    )
    assert requests_mock.call_count == 0
    try:
        raise Exception("Handled exception")
    except Exception as e:
        crybaby.catch(e)
    assert requests_mock.call_count == 1
    for history in requests_mock.request_history:
        if history.__str__() == "POST https://slack.com/api/chat.postMessage":
            assert history.json()["channel"] == TEST_SLACK_CHANNEL_ID
            assert "Handled exception" in history.json()["text"]