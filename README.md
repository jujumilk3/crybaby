# crybaby
🥲 Micro Python exception handler that sends error messages to Slack. 🚨

## Installation
```bash
pip install crybaby
```

## Example
```python
import crybaby


def unhandled_exception():
    raise Exception("Unhandled exception")


def handled_exception():
    try:
        raise Exception("Handled exception")
    except Exception as e:
        crybaby.catch(e)


if __name__ == "__main__":
    crybaby.setup(
        slack_token="xoxb-sample-slack-token", slack_channel_id="SLACKCHANNELID"
    )
    handled_exception()
    unhandled_exception()
```
Then

![slack_example.png](https://github.com/jujumilk3/crybaby/blob/main/doc/slack_example.png?raw=true)
