import json
import boto3
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import quote

ssm = boto3.client('ssm')

def lambda_handler(event, context):
    print(json.dumps(event))
    
    message = json.loads(event['Records'][0]['Sns']['Message'])
    print(json.dumps(message))
    
    alarm_name = message['AlarmName']
    new_state = message['NewStateValue']
    old_state = message['OldStateValue']
    reason = message['NewStateReason']
    region = message['AlarmArn'].split(':')[3]
    
    slack_message = {
        'text': f':fire: {alarm_name} state has changed from {old_state} to {new_state}\n> {reason}\n'
                'View this alarm in the AWS Management Console:\n'
                f'https://us-east-1.console.aws.amazon.com/cloudwatch/deeplink.js?region={region}#alarmsV2:alarm/{quote(alarm_name)}'
    }
                    
    webhook_url = ssm.get_parameter(Name='slackwebhookurl', WithDecryption=True)
    req = Request(webhook_url['Parameter']['Value'],
                    json.dumps(slack_message).encode('utf-8'))
    
    try:
        response = urlopen(req)
        response.read()
        print("Messge posted to Slack")
    except HTTPError as e:
        print(f'Request failed: {e.code} {e.reason}')
    except URLError as e:
        print(f'Server Connection failed:  {e.reason}')
