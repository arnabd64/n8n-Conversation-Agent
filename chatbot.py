import json
import os

import dotenv
import httpx

assert dotenv.load_dotenv(".env")

SESSION_ID_URL = os.getenv("SESSION_ID_URL")
CHAT_WORKFLOW_URL = os.getenv("CHAT_WORKFLOW_URL")
CHAT_HISTORY_URL = os.getenv("CHAT_HISTORY_URL")
BACKUP_HISTORY_URL = os.getenv("BACKUP_HISTORY_URL")


class Chatbot:
    """
    Class that abstracts logic from the Chainlit
    application. Each chat session has it's own
    instance of this class which can be identified
    using their `session_id`.

    Attributes:
        - `session_id` (str) : Unique Identifier for each session
    """
    def __init__(self, session_id: str):
        self.session_id = session_id

    @classmethod
    async def new_session(cls):
        """
        Factory function that initiates a new
        session by deriving a session id from n8n
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(SESSION_ID_URL)
            response.raise_for_status()
        return Chatbot(response.text)

    async def send_message(self, user_message: str) -> str:
        """
        Function that is Triggered after the user
        inputs a new message in the chainlit application.

        Attributes:
            - `message` (str) : User's Message

        Returns:
            - `ai_message` (str) : LLM's Message
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=CHAT_WORKFLOW_URL,
                json={"sessionId": self.session_id, "chatInput": user_message},
                timeout=300,
            )
            response.raise_for_status()
        return response.json()[0]["output"]

    async def get_chat_history(self) -> list[dict]:
        """
        Retrieves the chat history from redis database
        used to save chat message history for a particular
        session.

        Returns:
            - `chat_history` (list) : Chat History for `session_id`
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"{CHAT_HISTORY_URL}?sessionId={self.session_id}", timeout=300
            )
            response.raise_for_status()
        return [json.loads(item) for item in response.json()["history"]]

    async def backup_chat_history(self, history: list[dict]):
        """
        Executes the Backup-Chat-History workflow on n8n,
        which backs up chat history from redis to mongo db

        Attributes:
            - `history` (list) : Chat History
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{BACKUP_HISTORY_URL}?sessionId={self.session_id}",
                json={"history": history},
                timeout=300,
            )
            response.raise_for_status()
