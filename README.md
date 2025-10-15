# Conversation Agent Workflow using n8n

[n8n](https://n8n.io) is a low code automation platform which can be used to build AI Agents by simple `drag-n-drop` without diving into code. This feature of n8n makes making agents faster in comparison to langchain or langgraph. We don't need to create APIs for our agents since n8n provides us with webhooks.

The UI is built using [chainlit](https://github.com/Chainlit/chainlit) with is a UI framework for python which is designed for building UIs for chatbots and agents.

This respository demonstrates a simple *one-to-one* conversation agent using redis server for chat memory.

## Important

* Generate a secret token for chainlit by running the command: `chainlit create-secret`. Copy the secret to your `.env` file.