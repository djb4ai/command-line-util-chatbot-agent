# command-line-util-chatbot-agent
Chatbot Agent's CLI
## Installation

```bash
pip install .
```

## Usage

```bash
# Start a new conversation
warroom new [--name CONV_NAME] [--model MODEL]

# List conversations
warroom list

# Continue a conversation
warroom chat CONV_NAME

# Delete a conversation
warroom delete CONV_NAME
```

## Configuration

Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'
```
