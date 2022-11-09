import pytest

TEST_SLACK_TOKEN = "TEST_SLACK_TOKEN"
TEST_SLACK_CHANNEL_ID = "TEST_SLACK_CHANNEL_ID"


@pytest.fixture(scope="function", autouse=True)
def set_up(requests_mock):
    requests_mock.get(
        "https://slack.com/api/conversations.list",
        json={
            "ok": True,
            "channels": [
                {"id": "C01", "name": "general", "is_member": True},
                {"id": "C02", "name": "random", "is_member": True},
                {"id": "C03", "name": "test", "is_member": False},
                {"id": TEST_SLACK_CHANNEL_ID, "name": "test2", "is_member": True},
            ],
        },
    )
    requests_mock.post(
        "https://slack.com/api/chat.postMessage",
        json={"ok": True, "channel": TEST_SLACK_CHANNEL_ID, "ts": "1234567890.123456"},
    )
