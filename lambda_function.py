import os
import json
import logging
import urllib
import hashlib
import hmac
from botocore.vendored import requests
import json

# Grab the Bot OAuth token from the environment.
BOT_TOKEN = os.environ["BOT_TOKEN"]
slack_signing_secret = os.environ["SIGNING_SECRET"]

# Define the URL of the targeted Slack API resource.
# We'll send our replies there.
SLACK_URL = "https://slack.com/api/chat.postMessage"

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

''' Verify the POST request. '''
def verify_slack_request(slack_signature=None, slack_request_timestamp=None, request_body=None):
    ''' Form the basestring as stated in the Slack API docs. We need to make a bytestring. '''
    
    basestring = f"v0:{slack_request_timestamp}:{request_body}".encode('utf-8')

    ''' Make the Signing Secret a bytestring too. '''
    slack_signing_secret_bytes = bytes(slack_signing_secret, 'utf-8')

    ''' Create a new HMAC "signature", and return the string presentation. '''
    my_signature = 'v0=' + hmac.new(slack_signing_secret_bytes, basestring, hashlib.sha256).hexdigest()

    ''' Compare the the Slack provided signature to ours.
    If they are equal, the request should be verified successfully.
    Log the unsuccessful requests for further analysis
    (along with another relevant info about the request). '''
    if hmac.compare_digest(my_signature, slack_signature):
        return True
    else:
        logger.warning(f"Verification failed. my_signature: {my_signature}")
        return False


''' Process the POST request from API Gateway proxy integration. '''
def post(event, context):
    try:
        ''' Incoming data from Slack is application/x-www-form-urlencoded and UTF-8. '''

        ''' Capture the necessary data. '''
        slack_signature = event['headers']['X-Slack-Signature']
        slack_request_timestamp = event['headers']['X-Slack-Request-Timestamp']

        ''' Verify the request. '''
        if not verify_slack_request(slack_signature, slack_request_timestamp, event['body']):
            logger.info('Bad request.')
            response = {
                "statusCode": 400,
                "body": ''
            }
            return response

        body = event["body"]
        parsed_body = json.loads(body)
        print(parsed_body)
        this_event = parsed_body["event"]
        print(this_event)
        text = this_event["text"]
        
        # Get chemical descriptors of text, if possible
        apiurl = 'https://api.explorablelabs.com/descriptors/smiles/' + text
        headers = {'Content-Type': 'application/json'}
        r = requests.get(apiurl, headers=headers)
        print(r.status_code)
        print(r.text)
        descriptor_text = json.dumps(r.text)
        
        # We need to send back three pieces of information:
        #     1. The reversed text (text)
        #     2. The channel id of the private, direct chat (channel)
        #     3. The OAuth token required to communicate with 
        #        the API (token)
        # Then, create an associative array and URL-encode it, 
        # since the Slack API doesn't not handle JSON (bummer).
        
        # Get the ID of the channel where the message was posted.
        channel_id = this_event["channel"]
        
        #Hm, this is not working
        #response = {
        #    "statusCode": 200,
        #    "body": {
        #        "token": BOT_TOKEN,
        #        "channel": channel_id,
        #        "text": descriptor_text
        #    }
        #}
        #return response
        
        data = urllib.parse.urlencode(
            (
                ("token", BOT_TOKEN),
                ("channel", channel_id),
                ("text", descriptor_text)
            )
        )
        data = data.encode("ascii")
        
        # Construct the HTTP request that will be sent to the Slack API.
        request = urllib.request.Request(
            SLACK_URL, 
            data=data, 
            method="POST"
        )
        # Add a header mentioning that the text is URL-encoded.
        request.add_header(
            "Content-Type", 
            "application/x-www-form-urlencoded"
        )
        
        # Fire off the request!
        urllib.request.urlopen(request).read()

    except Exception as e:
        ''' Just a stub. Please make this better in real use :) '''
        logger.error(f"ERROR: {e}")
        response = {
            "statusCode": 200,
            "body": ''
        }
        return response

def lambda_handler(data, context):
    """Handle an incoming HTTP request from a Slack chat-bot.
    """
    
    body = data["body"]
    parsed_body = json.loads(body)
    if "challenge" in parsed_body:
        response = {
            "statusCode": 200,
            "body": parsed_body["challenge"]
        }
        return response

    # Grab the Slack event data.
    print(parsed_body)
    slack_event = parsed_body['event']
    
    # We need to discriminate between events generated by 
    # the users, which we want to process and handle, 
    # and those generated by the bot.
    if "bot_id" in slack_event:
        logging.warn("Ignore bot event")
    else:
        post(data, context)
        
    # Everything went fine.
    return "200 OK"
    
