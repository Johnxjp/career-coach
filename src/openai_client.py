"""
OpenAI Chat Client
Handles communication with OpenAI's API for chat completions.
"""

import os
from typing import Dict, List, Literal, Optional, Tuple

from openai import OpenAI

from src.prompts import system_message, client_message

ROLE = Literal["assistant", "user"]


class OpenAIClient:
    """Simple OpenAI client for chat completions"""

    def __init__(self, api_key: str, model: str = "gpt-4.1-nano"):
        """
        Initialize OpenAI client with environment variables

        Note: model parameter is used only in the OpenAI API call, and
        so can be adjusted as needed. For more advanced usage, you can
        select different models or configurations based on your needs.
        """
        self.model = model
        self.api_key = api_key

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = OpenAI(api_key=self.api_key)
        self.system_message: Optional[str] = system_message

    # def set_system_message(self, content: str):
    #     """
    #     Set a system message to define the assistant's behavior

    #     Args:
    #         content: The content of the system message
    #     """
    #     self.system_message = content

    def _get_chat_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Get a chat response from OpenAI

        Args:
            messages: List of message tuples with 'role' and 'content'

        Returns:
            The assistant's response text

        Raises:
            Exception: If the API call fails
        """
        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=self.system_message,
                input=messages,
                max_output_tokens=1000,
                temperature=0.7,
            )
            print(f"Calling OpenAI API with model: {self.model}")
            return response.output_text

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def format_messages(self, messages: List[Tuple[ROLE, str]]) -> List[Dict[str, str]]:
        """
        Format messages for OpenAI API

        Args:
            messages: List of tuples containing role and content

        Returns:
            List of dictionaries with 'role' and 'content'
        """
        messages = [{"role": role, "content": content} for role, content in messages]
        return messages

    def get_response_for_chat(self, messages: List[Tuple[ROLE, str]]) -> str:
        """
        Get a response for the chat application

        Args:
            messages: All messages in the chat history, including user and assistant messages in chronological order

        Returns:
            The assistant's response
        """

        # TODO: Manage context length of input messages
        messages = self.format_messages(messages)
        return self._get_chat_response(messages)


def get_openai_client() -> OpenAIClient:
    """
    Create an OpenAI client instance

    Returns:
        OpenAIClient instance configured with environment variables
    """
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    api_key = os.getenv("OPENAI_API_KEY")
    return OpenAIClient(api_key=api_key, model=model)
