import crybaby
from .conftest import TEST_SLACK_CHANNEL_ID, TEST_SLACK_TOKEN


def test_one_plus_one():
    assert 1 + 1 == 2


def test_setup(requests_mock):
    crybaby.setup(
        slack_token=TEST_SLACK_TOKEN, slack_channel_id=TEST_SLACK_CHANNEL_ID
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
