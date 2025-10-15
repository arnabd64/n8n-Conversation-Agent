import chainlit as ct

from chatbot import Chatbot


@ct.password_auth_callback
async def password_authentication(username: str, password: str):
    if (username, password) == ("admin", "admin"):
        return ct.User(username)


@ct.on_chat_start
async def init_chatbot():
    chatbot = await Chatbot.new_session()
    ct.user_session.set("id", chatbot.session_id)
    ct.user_session.set("chatbot", chatbot)

@ct.on_chat_end
async def fetch_chat_history():
    chatbot: Chatbot = ct.user_session.get("chatbot")
    chat_history = await chatbot.get_chat_history()
    if len(chat_history) > 0:
        await chatbot.backup_chat_history(chat_history)

@ct.on_message
async def chat_workflow(message: ct.Message):
    # get chatbot instance
    chatbot: Chatbot = ct.user_session.get("chatbot")

    # get chat response
    response = await chatbot.send_message(message.content)

    await ct.Message(response).send()
