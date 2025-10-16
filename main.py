"""
Chainlit Application
"""
import chainlit as ct

from chatbot import Chatbot


@ct.password_auth_callback
async def password_authentication(username: str, password: str):
    """
    Adds a login screen to the application
    """
    if (username, password) == ("admin", "admin"):
        return ct.User(username)


@ct.on_chat_start
async def init_chatbot():
    """
    Method to execute when a new chat session has
    been initiated.
    """
    chatbot = await Chatbot.new_session()
    ct.user_session.set("id", chatbot.session_id)
    ct.user_session.set("chatbot", chatbot)


@ct.on_chat_end
async def fetch_chat_history():
    """
    Method to execute when an existing chat session
    has been terminated.
    """
    chatbot: Chatbot = ct.user_session.get("chatbot")
    chat_history = await chatbot.get_chat_history()
    if len(chat_history) > 0:
        await chatbot.backup_chat_history(chat_history)


@ct.on_message
async def chat_workflow(message: ct.Message):
    """
    Method to execute when the user inputs a
    new chat message.
    """
    # get chatbot instance
    chatbot: Chatbot = ct.user_session.get("chatbot")

    # get chat response
    response = await chatbot.send_message(message.content)

    await ct.Message(response).send()
