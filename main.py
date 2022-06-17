import os
import sys
import time
import datetime
from slack import WebClient
from slack.errors import SlackApiError

TIME_OFFSET = 9
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
SLACK_FETCH_LIMIT = 1000

def fromtimestamp(ts, offset=0):
    dt = datetime.datetime.fromtimestamp(ts)
    delta = datetime.timedelta(hours=abs(offset))
    if TIME_OFFSET >= 0:
        return dt + delta
    else:
        return dt - delta

def print_message(message):
    if 'user_profile' in message and 'display_name' in message['user_profile']:
        name = message['user_profile']['display_name']
    elif 'username' in message:
        name = message['username']
    else:
        name = message['user']

    dt = fromtimestamp(float(message['ts']), TIME_OFFSET)

    print("{name}  {time}\n{text}\n".format(name=name, time=dt.strftime("%Y-%m-%d %H:%M:%S"), text=message['text']))

if __name__ == '__main__':
    slack_client = WebClient(token=os.environ['SLACK_API_TOKEN'])
    
    messages = []
    next_cursor = ''
    
    while True:
        response = None

        try:
            params = {}
            if next_cursor:
                params = {'cursor': next_cursor}
            response = slack_client.conversations_history(channel=SLACK_CHANNEL, limit=SLACK_FETCH_LIMIT, **params)

            messages.extend(response['messages'])
        except SlackApiError as e:
            print(e, file=sys.stderr)
            sys.exit(1)

        if response['has_more'] and response['response_metadata'] and response['response_metadata']['next_cursor']:
            next_cursor = response['response_metadata']['next_cursor']
        else:
            break
        time.sleep(1)

    for message in reversed(messages):
        print_message(message)
