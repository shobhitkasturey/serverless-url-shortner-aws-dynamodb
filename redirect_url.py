import json 
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("URLShortner")

def lambda_handler(event, context):
    try:
      short_id = event["pathParameters"]["short_id"]
      response = table.get_item(Key={"short_id": short_id})

      if "Item" not in response:
         return {
            "statusCode": 404,
            "body": json.dumps({"error": "URL not found"})
         }
      
      return{
         "statusCode": 302,
         "headers": {"Location" : response["Item"]["original_url"]}
      }
    

    except Exception as e:
       return {
          "statusCode": 500,
          "body": json.dumps({"error": str(e)})
       }
     