# command-line-util-chatbot-agent
Chatbot Agent's CLI
## Installation

```bash
pip install .
```

## Usage

```bash
# Start a new conversation
ai new [--name CONV_NAME] [--model MODEL]

# List conversations
ai list

# Continue a conversation
ai chat CONV_NAME

# Delete a conversation
ai delete CONV_NAME
```

## Configuration

Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'
```
