from abc import ABC, abstractmethod
from typing import Optional, List
from pydantic import BaseModel


class ChatMessage(BaseModel):
    is_agent: bool = False
    agent_name: Optional[str] = None
    content: str = None
    timestamp: int = None


class ChatContext(BaseModel):
    chat_session_id: str = None
    note: Optional[str] = None
    # TODO: Related notes of the same patient.
    # TODO: More structural information about the patient.


class AgentResponse(BaseModel):
    messages: List[str] = []
    storage: dict = None


class Bridge(ABC):
    @abstractmethod
    def on_receive(self,
                   message_stack: List[ChatMessage],
                   context: ChatContext,
                   storage: dict) -> AgentResponse:
        """
        The callback function when the agent receives a message.

        Parameters
        ----------
        message_stack : List[ChatMessage]
            The message stack that contains all the messages in the chat, where the last item is the new message.
        context : ChatContext
            The context of the conversation.
        storage : dict
            The storage of the agent. It is a dictionary that can be used to store any information.
            The dictionary will be passed based on the chat session id.

        Returns
        -------
        AgentResponse
            The response of the agent. It includes a list of messages and the dictionary to be stored.

        """
        pass
