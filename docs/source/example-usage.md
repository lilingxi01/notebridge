# Example usage

```python
from typing import List

from notebridge import Bridge, ChatMessage, ChatContext, AgentResponse
import openai


class MyAgent(Bridge):
    def on_receive(self,
                   message_stack: List[ChatMessage],
                   context: ChatContext,
                   storage: dict) -> AgentResponse:
        # TODO: Implement your agent here.
        # You can access environment variables by using something like `os.environ['OPENAI_API_KEY']`.

        gpt_messages = [{
            "role": "system",
            "content": f'You are role-playing as a physician called NoteAid, who can answer patients\' questions about their health. Here is patient\'s clinical note: {context.note}',
        }]

        for prev_message in message_stack:
            if prev_message.is_agent:
                gpt_messages.append({
                    "role": "assistant",
                    "content": prev_message.content,
                })
            else:
                gpt_messages.append({
                    "role": "user",
                    "content": prev_message.content,
                })

        chat_completion = openai.ChatCompletion.create(model='gpt-4', messages=gpt_messages)
        answer = chat_completion.choices[0].message.content

        # `messages` is a list of messages that you want to send back to the user.
        # `storage` is a dictionary that you can use to store data between different requests.
        # You need to pass the dict into here in order to access it in the next request.
        return AgentResponse(messages=[answer], storage=storage)
```