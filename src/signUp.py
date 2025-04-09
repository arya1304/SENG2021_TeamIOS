import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DespatchAdviceUsers') # table name might change
    username = event.get('username')
    password = event.get('password')

    #need to hash the pass word and place it securley
    if not username:
        return {
            "statusCode": 400,
            "message": "Bad Request - username not provided"
        }
    
    if not password:
        return {
            "statusCode": 400,
            "message": "Bad Request - password not provided"
        }
    
    #make the username a key in the table
    user_item = {
        'username': username,
        'password': password
    }

    table.put_item(Item=user_item)

    return {
        "statusCode": 200,
        "message" : "Congratualtions you have signed up"
    }