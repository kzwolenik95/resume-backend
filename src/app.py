import boto3
import json

dynamo = boto3.client('dynamodb')

def respond(err, res=None):
    return {
        'statusCode': 400 if err else 200,
        'body': json.dumps(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
    }

def increment_counter():
    response = dynamo.update_item(
        TableName='counter_table',
        Key={
            'Id' : {
                'S': 'visit_counter'
            }
        },
        UpdateExpression='ADD counter_value :v',
        ExpressionAttributeValues={
            ":v": {"N": "1"}
        }
    )
    return response
    
def get_counter_value():
    response = dynamo.get_item(
        TableName='counter_table',
        Key={
            'Id': {
                'S': 'visit_counter'
                }
        }
    )
    return {'counter_value': response['Item']['counter_value']['N']}

def lambda_handler(event, context):
    
    print(f'Event: {json.dumps(event)}')
    
    resource_called = event['resource']
    method = event['httpMethod']
    
    if resource_called == '/health':
        return respond(None, {'status': 'OK'})
    elif resource_called == '/increment':
        if method == 'GET':
            resp = get_counter_value()
            return respond(None, resp)
        elif method == 'POST':
            resp = increment_counter()
            return respond(None, resp)
        else:
            return respond('Wrong call')
    else:
        return respond('Wrong call')