# Conversation Agent Workflow using n8n

[n8n](https://n8n.io) is a low code automation platform which can be used to build AI Agents by simple `drag-n-drop` without diving into code. This feature of n8n makes making agents faster in comparison to langchain or langgraph. We don't need to create APIs for our agents since n8n provides us with webhooks.

The UI is built using [chainlit](https://github.com/Chainlit/chainlit) with is a UI framework for python which is designed for building UIs for chatbots and agents.

This respository demonstrates a simple *one-to-one* conversation agent using redis server for chat memory.

## Getting Started

### Backend Servers

To run this application, you need to have a running instance of:

1. n8n
2. Redis *(For Short-Term Chat Memory)*
3. MongoDB *(Backup/Long-Term Chat Memory)*

### n8n Templates

Once the above step is complete, you can restore the workflows from the [n8n-workflows](./n8n-workflows/README.md). After the backup has been restored, you have to add your credentials for Redis and MongoDB.

### Frontend (*Chainlit*)

#### Step 1: Install Dependencies

##### Using `uv` (*Recommended*)

```bash
$ uv sync
```

##### Using `pip`

```bash
# create a virtual environment
$ python3 -m venv .venv
$ source .venv/bin/activate

# install dependencies from pyproject.toml
$ pip install -e .
```

#### Step 2: Create a `.env` file

Create a `.env` file which contains the **Webhook endpoints** for the n8n workflows. *You can checkout the `.env.example` file*

#### Step 3: Generate Secret for JWT

```bash
$ chainlit create-secret

# The output should be:
#
# Copy the following secret into your .env file. Once it is set, changing it will logout all users with active sessions.
# CHAINLIT_AUTH_SECRET="pWbD=EV7C%_D4:rs$nj5%~CUpetAd2i*uk~Y~J93y6dEMdeWdv/BW.bEWXEZ38H6"
```

**Note**: *Copy the `CHAINLIT_AUTH_SECRET` line to your .env file*

#### Run the Application

```bash
# runs the server at http://127.0.0.1:8000
$ chainlit run main.py 

# change the host & port
$ chainlit run main.py --host=0.0.0.0 --port=8081
```

To gain access to the application you need to login using the username: `admin` and password: `admin`
