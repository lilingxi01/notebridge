import logging

from pydantic import ValidationError
from flask import jsonify, request

from .bridge import ChatMessage, ChatContext, Bridge
from .hello_page import hello_page_html


def make_executor(agent: Bridge):
    """
    This function is used to create an executor function that can be used as a Lambda handler.
    """
    def inner_adapter():
        if request.method == 'GET':
            return hello_page_html

        body = request.get_json()

        if body is None:
            return jsonify(error="Missing JSON parameters"), 400

        if 'message_stack' not in body or type(body['message_stack']) != list:
            return jsonify(error="Message stack (message_stack) is invalid from the request."), 400

        if 'context' not in body or type(body['context']) != dict:
            return jsonify(error="Context (context) is invalid from the request."), 400

        try:
            message_stack = [ChatMessage(**m) for m in body['message_stack']]
            context = ChatContext(**body['context'])
            storage = body['storage'] if 'storage' in body else dict()
        except ValidationError as e:
            logging.error(f"Error occurred while parsing the request: {str(e)}")
            return jsonify(error="Invalid JSON parameters"), 400

        response = agent.on_receive(message_stack=message_stack, context=context, storage=storage)

        # TODO: We might want to make responses async in future versions.
        return jsonify({
            "response": response.messages,
            "storage": response.storage
        })

    return inner_adapter
