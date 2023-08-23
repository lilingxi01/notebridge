from abc import ABC, abstractmethod
from typing import Optional, List, Union
from pydantic import BaseModel


class ChatMessage(BaseModel):
    is_agent: bool = False
    agent_name: Optional[str] = None
    content: str = None
    timestamp: int = None


class ChatContext(BaseModel):
    note: Optional[str] = None
    # TODO: Related notes of the same patient.
    # TODO: More structural information about the patient.


class Bridge(ABC):
    @abstractmethod
    def on_receive(self, message_stack: List[ChatMessage], context: ChatContext) -> Union[str, List[str]]:
        """
        The callback function when the agent receives a message.

        Parameters
        ----------
        message_stack : List[ChatMessage]
            The message stack that contains all the messages in the chat, where the last item is the new message.
        context : ChatContext
            The context of the conversation.

        Returns
        -------
        Union[str, List[str]]
            The response of the agent. It could be one message (string) or a list of messages (list of strings).

        """
        pass
