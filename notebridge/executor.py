import json
import logging

from pydantic import ValidationError

from .bridge import ChatMessage, ChatContext, Bridge


def make_executor(agent: Bridge):
    """
    This function is used to create an executor function that can be used as a Lambda handler.
    """
    def inner_adapter(event, context):
        if 'body' not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Request body is missing."
                })
            }

        body = event['body']

        if 'message_stack' not in body or type(body['message_stack']) != list:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Message stack (message_stack) is invalid from the request."
                })
            }

        if 'context' not in body or type(body['context']) != dict:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Context (context) is invalid from the request."
                })
            }

        try:
            message_stack = [ChatMessage(**m) for m in body['message_stack']]
            context = ChatContext(**body['context'])
            storage = body['storage'] if 'storage' in body else dict()
        except ValidationError as e:
            logging.error(f"Error occurred while parsing the request: {str(e)}")
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"Invalid message_stack or context structure: {str(e)}"
                })
            }

        response = agent.on_receive(message_stack=message_stack, context=context, storage=storage)

        # TODO: We might want to make responses async in future versions.
        return {
            "statusCode": 200,
            "body": json.dumps({
                "response": response.messages,
                "storage": response.storage
            })
        }

    return inner_adapter
