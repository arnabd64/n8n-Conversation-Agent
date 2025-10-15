import os
import json
import dotenv
import httpx

assert dotenv.load_dotenv(".env")

SESSION_ID_URL = os.getenv("SESSION_ID_URL")
CHAT_WORKFLOW_URL = os.getenv("CHAT_WORKFLOW_URL")
CHAT_HISTORY_URL = os.getenv("CHAT_HISTORY_URL")
BACKUP_HISTORY_URL = os.getenv("BACKUP_HISTORY_URL")


class Chatbot:
    def __init__(self, session_id: str):
        self.session_id = session_id

    @classmethod
    async def new_session(cls):
        async with httpx.AsyncClient() as client:
            response = await client.get(SESSION_ID_URL)
            response.raise_for_status()
        return Chatbot(response.text)

    async def send_message(self, message: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=CHAT_WORKFLOW_URL,
                json={"sessionId": self.session_id, "chatInput": message},
                timeout=300,
            )
            response.raise_for_status()
        return response.json()[0]["output"]
    
    async def get_chat_history(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url = f"{CHAT_HISTORY_URL}?sessionId={self.session_id}",
                timeout=300
            )
            response.raise_for_status()
        return [json.loads(item) for item in response.json()["history"]]
    
    async def backup_chat_history(self, history: list[dict]):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url = f"{BACKUP_HISTORY_URL}?sessionId={self.session_id}",
                json = {"history": history},
                timeout = 300
            )
            response.raise_for_status()
