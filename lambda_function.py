import json
import boto3
import hashlib

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("URLShortner")

def lambda_handler(event, context):
    try:
        
        body = json.loads(event.get("body", "{}"))
        
        if "url" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'url' parameter"})
            }

        long_url = body["url"]

        
        short_id = hashlib.md5(long_url.encode()).hexdigest()[:6]

     
        table.put_item(Item={"short_id": short_id, "original_url": long_url})

        return {
            "statusCode": 200,
            "body": json.dumps({"short_url": f"https://short.ly/{short_id}"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
